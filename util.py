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


class AuthInfo(object):

    ACCESS_TOKEN = None
    ROOT_CERTIFICATES = None


def protobuf_to_dict(pb_value):
    result = {}
    for name in pb_value.DESCRIPTOR.fields_by_name.keys():
        value = getattr(pb_value, name)
        if isinstance(
                value,
                internal.containers.RepeatedCompositeFieldContainer):
            value = list(value)
        result[name] = value
    return result


def print_debug_info(value):
    if not os.environ.has_key('VERBOSE'):
        return
    print('==DEBUG INFO: %s' % (value,))


def _set_token():
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
    if AuthInfo.ACCESS_TOKEN is None or reset:
        _set_token()


def get_token():
    set_token(reset=False)
    return AuthInfo.ACCESS_TOKEN


def _set_certs():
    with open(SSL_CERT_FILE, mode='rb') as file_obj:
        AuthInfo.ROOT_CERTIFICATES = file_obj.read()


def set_certs(reset=False):
    if AuthInfo.ROOT_CERTIFICATES is None or reset:
        _set_certs()


def get_certs():
    set_certs(reset=False)
    return AuthInfo.ROOT_CERTIFICATES
