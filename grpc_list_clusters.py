"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Cluster Admin API to list clusters.
"""

from util import make_cluster_request


if __name__ == '__main__':
    make_cluster_request('ListClusters', pretty_print=True)
