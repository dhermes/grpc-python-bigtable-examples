from gcloud_bigtable._generated import bigtable_cluster_service_messages_pb2
from gcloud_bigtable._generated import bigtable_cluster_service_pb2

STUB_CLASS = (bigtable_cluster_service_pb2.
              early_adopter_create_BigtableClusterService_stub)


TIMEOUT_SECONDS = 2
PROJECT_ID = '1234PROJECTID'
HOST = 'bigtabletableadmin.googleapis.com'
PORT = 443


stub = STUB_CLASS(HOST, PORT,
                  metadata_transformer=None,  # Auth might go here?
                  secure=True,
                  root_certificates=None, private_key=None,
                  certificate_chain=None, server_host_override=None)
with stub:
    request_pb = bigtable_cluster_service_messages_pb2.ListZonesRequest(
        name='projects/' + PROJECT_ID)
    response = stub.ListZones(request_pb, TIMEOUT_SECONDS)
