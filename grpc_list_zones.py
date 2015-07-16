"""Using gRPC to test gcloud-python-bigtable.

In this script, we use the Cluster Admin API to list zones.
"""

from __future__ import print_function

import json

from util import make_cluster_request
from util import protobuf_to_dict


def main():
    """Main function for executing script."""
    result_pb = make_cluster_request('ListZones')
    print('result type:')
    print(type(result_pb).__name__)
    print('result:')
    print(json.dumps(protobuf_to_dict(result_pb),
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
