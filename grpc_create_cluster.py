"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Cluster Admin API to list clusters.
"""

from __future__ import print_function

from gcloud_bigtable._generated import bigtable_cluster_data_pb2 as data_pb2
from gcloud_bigtable._generated import (
    bigtable_cluster_service_messages_pb2 as messages_pb2)

from config import CLUSTER
from config import PROJECT_ID
from config import ZONE
from util import make_cluster_request


def main():
    zone_full_name = 'projects/%s/zones/%s' % (PROJECT_ID, ZONE)
    # From the .proto definition of CreateClusterRequest: the "name",
    # "delete_time", and "current_operation" fields must be left blank.
    cluster = data_pb2.Cluster(display_name=CLUSTER, serve_nodes=3)
    request_pb = messages_pb2.CreateClusterRequest(
        name=zone_full_name,
        cluster_id=CLUSTER,
        cluster=cluster,
    )
    result_pb = make_cluster_request('CreateCluster',
                                     request_pb=request_pb)
    print(result_pb)


if __name__ == '__main__':
    main()
