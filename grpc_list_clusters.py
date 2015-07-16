"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Cluster Admin API to list clusters.
"""

from __future__ import print_function

import json

from gcloud_bigtable._generated import bigtable_cluster_service_messages_pb2

from config import PROJECT_ID
from config import TIMEOUT_SECONDS
from util import PORT
from util import CLUSTER_ADMIN_HOST as HOST
from util import CLUSTER_STUB_FACTORY as STUB_FACTORY
from util import custom_metadata_transformer
from util import get_certs
from util import protobuf_to_dict


def main():
    """Main function for executing script."""
    stub = STUB_FACTORY(HOST, PORT,
                        metadata_transformer=custom_metadata_transformer,
                        secure=True,
                        root_certificates=get_certs())

    project_name = 'projects/%s' % (PROJECT_ID,)
    request_pb = bigtable_cluster_service_messages_pb2.ListClustersRequest(
        name=project_name)
    result_pb = None
    with stub:
        response = stub.ListClusters.async(request_pb, TIMEOUT_SECONDS)
        result_pb = response.result()

    print('result type:')
    print(type(result_pb).__name__)
    print('result:')
    print(json.dumps(protobuf_to_dict(result_pb),
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
