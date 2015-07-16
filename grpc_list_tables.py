"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Table Admin API to list tables in a cluster.
"""

from __future__ import print_function

import json

from gcloud_bigtable._generated import bigtable_table_service_messages_pb2
from gcloud_bigtable._generated import bigtable_table_service_pb2

from config import CLUSTER
from config import PROJECT_ID
from config import TIMEOUT_SECONDS
from config import ZONE
from util import PORT
from util import TABLE_ADMIN_HOST as HOST
from util import custom_metadata_transformer
from util import get_certs
from util import protobuf_to_dict


STUB_FACTORY = (bigtable_table_service_pb2.
                early_adopter_create_BigtableTableService_stub)


stub = STUB_FACTORY(HOST, PORT,
                    metadata_transformer=custom_metadata_transformer,
                    secure=True,
                    root_certificates=get_certs())

table_name = 'projects/%s/zones/%s/clusters/%s' % (
    PROJECT_ID, ZONE, CLUSTER)
request_pb = bigtable_table_service_messages_pb2.ListTablesRequest(
    name=table_name)
result_pb = None
with stub:
    response = stub.ListTables.async(request_pb, TIMEOUT_SECONDS)
    result_pb = response.result()

print('result type:')
print(type(result_pb).__name__)
print('result:')
print(json.dumps(protobuf_to_dict(result_pb),
                 indent=2, sort_keys=True))
