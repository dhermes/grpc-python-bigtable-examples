"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Cluster Admin API to list zones.
"""

from __future__ import print_function

import json

from gcloud_bigtable._generated import bigtable_cluster_service_messages_pb2
from gcloud_bigtable._generated import bigtable_cluster_service_pb2

from config import PROJECT_ID
from config import TIMEOUT_SECONDS
from util import PORT
from util import CLUSTER_ADMIN_HOST as HOST
from util import get_certs
from util import get_token
from util import protobuf_to_dict


STUB_FACTORY = (bigtable_cluster_service_pb2.
                early_adopter_create_BigtableClusterService_stub)


def custom_metadata_transformer(ignored_val):
    """Adds authorization header to request metadata."""
    return [('Authorization', 'Bearer ' + get_token())]


stub = STUB_FACTORY(HOST, PORT,
                    metadata_transformer=custom_metadata_transformer,
                    secure=True,
                    root_certificates=get_certs())

project_name = 'projects/%s' % (PROJECT_ID,)
request_pb = bigtable_cluster_service_messages_pb2.ListZonesRequest(
    name=project_name)
result_pb = None
with stub:
    response = stub.ListZones.async(request_pb, TIMEOUT_SECONDS)
    result_pb = response.result()

print('result type:')
print(type(result_pb).__name__)
print('result:')
print(json.dumps(protobuf_to_dict(result_pb),
                 indent=2, sort_keys=True))
