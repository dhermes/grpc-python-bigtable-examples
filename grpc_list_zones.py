"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Cluster Admin API to list zones.
"""

from __future__ import print_function

import json

from gcloud_bigtable._generated import bigtable_cluster_service_messages_pb2

from config import PROJECT_ID
from config import TIMEOUT_SECONDS
from util import make_cluster_stub
from util import protobuf_to_dict


def main():
    """Main function for executing script."""
    stub = make_cluster_stub()
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


if __name__ == '__main__':
    main()
