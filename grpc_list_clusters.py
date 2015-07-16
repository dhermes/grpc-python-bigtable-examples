"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Cluster Admin API to list clusters.
"""

from util import pretty_print_cluster_result


if __name__ == '__main__':
    pretty_print_cluster_result('ListClusters')
