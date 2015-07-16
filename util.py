"""Utility library for gcloud-python-bigtable test scripts."""

from __future__ import print_function

import os

from google.protobuf import internal
from oauth2client.client import GoogleCredentials
from oauth2client.client import _get_application_default_credential_from_file

from gcloud_bigtable._generated import bigtable_cluster_service_messages_pb2
from gcloud_bigtable._generated import bigtable_cluster_service_pb2
from gcloud_bigtable._generated import bigtable_table_service_pb2

from config import KEYFILE_PATH
from config import PROJECT_ID
from config import TIMEOUT_SECONDS


BASE_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.data'
TABLE_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.admin'
CLUSTER_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.admin'
CLOUD_PLATFORM_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'
SSL_CERT_FILE = '/etc/ssl/certs/ca-certificates.crt'
PORT = 443
TABLE_ADMIN_HOST = 'bigtabletableadmin.googleapis.com'
CLUSTER_ADMIN_HOST = 'bigtableclusteradmin.googleapis.com'
TABLE_STUB_FACTORY = (bigtable_table_service_pb2.
                      early_adopter_create_BigtableTableService_stub)
CLUSTER_STUB_FACTORY = (bigtable_cluster_service_pb2.
                        early_adopter_create_BigtableClusterService_stub)
_BASE_TYPES = (bool, int, long, float, bytes, unicode,
               list, tuple, type(None))


class AuthInfo(object):
    """Local namespace for caching auth information."""

    ACCESS_TOKEN = None
    ROOT_CERTIFICATES = None


def protobuf_to_dict(pb_value):
    """Converts a protobuf value to a dictionary."""
    result = {}
    for name in pb_value.DESCRIPTOR.fields_by_name.keys():
        value = getattr(pb_value, name)
        # Convert repeated to lists.
        if isinstance(
                value,
                internal.containers.RepeatedCompositeFieldContainer):
            value = list(value)
        # Convert complex types to dict.
        if not isinstance(value, _BASE_TYPES):
            value = protobuf_to_dict(value)
        # Convert repeated complex types to dict.
        if isinstance(value, (list, tuple)):
            value_as_list = []
            for entry in value:
                if not isinstance(entry, _BASE_TYPES):
                    entry = protobuf_to_dict(entry)
                value_as_list.append(entry)
            value = value_as_list
        result[name] = value
    return result


def print_debug_info(value):
    """Method for optionally printing debug information.

    Only prints if the user has set the VERBOSE environment variable.
    """
    if not os.environ.has_key('VERBOSE'):
        return
    print('==DEBUG INFO: %s' % (value,))


def _set_token():
    """Sets the cached auth. token locally.

    Uses a service account by default but uses the `gcloud login`
    application default credentials if the USE_APP_DEFAULT
    environment variable has been set.
    """
    if os.environ.has_key('USE_APP_DEFAULT'):
        print_debug_info('Setting token from Application Default Credentials')
        credentials = GoogleCredentials.get_application_default()
        scoped_credentials = credentials.create_scoped(CLOUD_PLATFORM_SCOPE)
    else:
        print_debug_info('Setting token from Service Account Credentials')
        credentials = _get_application_default_credential_from_file(
            KEYFILE_PATH)
        scoped_credentials = credentials.create_scoped(
            [BASE_SCOPE, TABLE_SCOPE, CLUSTER_SCOPE])

    AuthInfo.ACCESS_TOKEN = scoped_credentials.get_access_token().access_token


def set_token(reset=False):
    """Sets the cached auth. token locally.

    If not manually told to reset or if the value is already set,
    does nothing.
    """
    if AuthInfo.ACCESS_TOKEN is None or reset:
        _set_token()


def get_token():
    """Gets the cached auth. token.

    Calls set_token() first in case the value has not been set, but
    this will do nothing if the value is already set.
    """
    set_token(reset=False)
    return AuthInfo.ACCESS_TOKEN


def _set_certs():
    """Sets the cached root certificates locally."""
    with open(SSL_CERT_FILE, mode='rb') as file_obj:
        AuthInfo.ROOT_CERTIFICATES = file_obj.read()


def set_certs(reset=False):
    """Sets the cached root certificates locally.

    If not manually told to reset or if the value is already set,
    does nothing.
    """
    if AuthInfo.ROOT_CERTIFICATES is None or reset:
        _set_certs()


def get_certs():
    """Gets the cached root certificates.

    Calls set_certs() first in case the value has not been set, but
    this will do nothing if the value is already set.
    """
    set_certs(reset=False)
    return AuthInfo.ROOT_CERTIFICATES


def custom_metadata_transformer(ignored_val):
    """Adds authorization header to request metadata."""
    return [('Authorization', 'Bearer ' + get_token())]


def make_cluster_stub():
    """Makes a stub for the Cluster Admin API."""
    return CLUSTER_STUB_FACTORY(
        CLUSTER_ADMIN_HOST, PORT,
        metadata_transformer=custom_metadata_transformer,
        secure=True,
        root_certificates=get_certs())


def make_table_stub():
    """Makes a stub for the Table Admin API."""
    return TABLE_STUB_FACTORY(
        TABLE_ADMIN_HOST, PORT,
        metadata_transformer=custom_metadata_transformer,
        secure=True,
        root_certificates=get_certs())


def make_cluster_request(method, project_id=PROJECT_ID,
                         timeout_seconds=TIMEOUT_SECONDS):
    """Make a gRPC request for ``method`` to the Cluster Admin API."""
    request_attr = '%sRequest' % (method,)
    request_pb_class = getattr(
        bigtable_cluster_service_messages_pb2,
        request_attr)

    project_name = 'projects/%s' % (project_id,)
    request_pb = request_pb_class(name=project_name)
    result_pb = None

    with make_cluster_stub() as stub:
        request_obj = getattr(stub, method)
        response = request_obj.async(request_pb, timeout_seconds)
        result_pb = response.result()

    return result_pb
