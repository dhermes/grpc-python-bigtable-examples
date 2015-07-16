"""Utility library for gcloud-python-bigtable test scripts."""

from __future__ import print_function

import os

from google.protobuf import internal
from oauth2client.client import GoogleCredentials
from oauth2client.client import _get_application_default_credential_from_file

from config import KEYFILE_PATH


BASE_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.data'
TABLE_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.admin'
CLUSTER_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.admin'
CLOUD_PLATFORM_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'
SSL_CERT_FILE = '/etc/ssl/certs/ca-certificates.crt'
PORT = 443
TABLE_ADMIN_HOST = 'bigtabletableadmin.googleapis.com'
CLUSTER_ADMIN_HOST = 'bigtableclusteradmin.googleapis.com'
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
