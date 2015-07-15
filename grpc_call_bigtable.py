import os
import traceback

from oauth2client.client import _get_application_default_credential_from_file

from gcloud_bigtable._generated import bigtable_cluster_service_messages_pb2
from gcloud_bigtable._generated import bigtable_cluster_service_pb2


PROJECT_ID = '1234PROJECTID'
JSON_PATH = 'path/to/credentials_file.json'

STUB_CLASS = (bigtable_cluster_service_pb2.
              early_adopter_create_BigtableClusterService_stub)
TABLE_SCOPE = 'https://www.googleapis.com/auth/bigtable.admin.table'
CLUSTER_SCOPE = 'https://www.googleapis.com/auth/bigtable.admin.cluster'
SSL_CERT_FILE = '/etc/ssl/certs/ca-certificates.crt'
CREDENTIALS = _get_application_default_credential_from_file(JSON_PATH)
SCOPED_CREDENTIALS = CREDENTIALS.create_scoped([TABLE_SCOPE, CLUSTER_SCOPE])
ACCESS_TOKEN = SCOPED_CREDENTIALS.get_access_token().access_token
del CREDENTIALS
del SCOPED_CREDENTIALS
AUTH_HEADER = 'Bearer ' + ACCESS_TOKEN
TIMEOUT_SECONDS = 2
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
request_pb = bigtable_cluster_service_messages_pb2.ListZonesRequest(
    name='projects/' + PROJECT_ID)
with stub:
    response = stub.ListZones.async(request_pb, TIMEOUT_SECONDS)

print('response.running():')
print(response.running())
print('response.done():')
print(response.done())
print('response.cancelled():')
print(response.cancelled())
print('response.exception():')
print(response.exception())
tb = response.traceback()
traceback.print_tb(tb)
response.result()
