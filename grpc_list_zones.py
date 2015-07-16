"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Cluster Admin API to list zones.
"""

from util import make_cluster_request


if __name__ == '__main__':
    make_cluster_request('ListZones', pretty_print=True)
