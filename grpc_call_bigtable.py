import os

from oauth2client.client import _get_application_default_credential_from_file

from gcloud_bigtable._generated import bigtable_table_service_messages_pb2
from gcloud_bigtable._generated import bigtable_table_service_pb2


PROJECT_ID = '1234PROJECTID'
JSON_PATH = 'path/to/credentials_file.json'
ZONE = 'us-central1-b'
CLUSTER = 'foo-bar-baz-1262357y324823'

STUB_CLASS = (bigtable_table_service_pb2.
              early_adopter_create_BigtableTableService_stub)
BASE_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.data'
TABLE_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.admin'
CLUSTER_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.admin'
SSL_CERT_FILE = '/etc/ssl/certs/ca-certificates.crt'
CREDENTIALS = _get_application_default_credential_from_file(JSON_PATH)
SCOPED_CREDENTIALS = CREDENTIALS.create_scoped([BASE_SCOPE, TABLE_SCOPE,
                                                CLUSTER_SCOPE])
ACCESS_TOKEN = SCOPED_CREDENTIALS.get_access_token().access_token
del CREDENTIALS
del SCOPED_CREDENTIALS
AUTH_HEADER = 'Bearer ' + ACCESS_TOKEN
TIMEOUT_SECONDS = 10
HOST = 'bigtabletableadmin.googleapis.com'
PORT = 443
with open(SSL_CERT_FILE, mode='rb') as file_obj:
    ROOT_CERTIFICATES = file_obj.read()


def custom_metadata_transformer(ignored_val):
    return [('Authorization', AUTH_HEADER)]


stub = STUB_CLASS(HOST, PORT,
                  metadata_transformer=custom_metadata_transformer,
                  secure=True,
                  root_certificates=ROOT_CERTIFICATES,
                  private_key=None,
                  certificate_chain=None,
                  server_host_override=None)

table_name = 'projects/%s/zones/%s/clusters/%s' % (
    PROJECT_ID, ZONE, CLUSTER)
request_pb = bigtable_table_service_messages_pb2.ListTablesRequest(
    name=table_name)
with stub:
    response = stub.ListTables.async(request_pb, TIMEOUT_SECONDS)
    print('response.running():')
    print(response.running())
    print('response.done():')
    print(response.done())
    print('response.cancelled():')
    print(response.cancelled())
    print('response.exception():')
    print(repr(response.exception()))
    print('response.result():')
    print(response.result())
