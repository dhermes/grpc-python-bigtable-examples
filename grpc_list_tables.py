"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Table Admin API to list tables in a cluster.
"""

from util import make_table_request


if __name__ == '__main__':
    make_table_request('ListTables', pretty_print=True)
