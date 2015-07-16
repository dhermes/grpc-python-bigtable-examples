import time

import grpc._adapter._intermediary_low as low_level

from gcloud_bigtable._generated import bigtable_cluster_service_messages_pb2
from gcloud_bigtable._generated import bigtable_cluster_service_pb2

from config import PROJECT_ID
from config import TIMEOUT_SECONDS
from util import PORT
from util import CLUSTER_ADMIN_HOST as HOST
from util import get_certs
from util import get_token


STUB_FACTORY = (bigtable_cluster_service_pb2.
                early_adopter_create_BigtableClusterService_stub)
EVENT_DICT = {}
HOST_PORT = '%s:%d' % (HOST, PORT)
PROJECT_NAME = 'projects/%s' % (PROJECT_ID,)
METHOD = ('/google.bigtable.admin.cluster.v1.'
          'BigtableClusterService/ListZones')


client_creds = low_level.ClientCredentials(
    root_certificates=get_certs(),
    private_key=None,
    certificate_chain=None)
channel = low_level.Channel(hostport=HOST_PORT,
                            client_credentials=client_creds,
                            server_host_override=None)
completion_queue = low_level.CompletionQueue()
request_pb = bigtable_cluster_service_messages_pb2.ListZonesRequest(
    name=PROJECT_NAME)
request_pb_as_str = request_pb.SerializeToString()
expire_timestamp = time.time() + TIMEOUT_SECONDS
call_obj = low_level.Call(channel=channel, completion_queue=completion_queue,
                          method=METHOD, host=HOST,
                          deadline=expire_timestamp)
call_obj.add_metadata(key='Authorization', value='Bearer ' + get_token())
# First request -- invoke means "begin the RPC connection"
invoke_result = call_obj.invoke(completion_queue=completion_queue,
                                metadata_tag='1:METADATA-TAG',
                                finish_tag='2:FINISH-TAG')
# Read the first event off the queue, expect to be METADATA_ACCEPTED
EVENT_DICT[1] = completion_queue.get(deadline=None)
# Second Request -- write request to connection
write_result = call_obj.write(message=request_pb_as_str, tag='3:WRITE-TAG')
# Read the second event off the queue
EVENT_DICT[2] = completion_queue.get(deadline=None)
# Third Request -- complete means "sending data now"
call_obj.complete(tag='4:COMPLETE-TAG')
# Read the third event off the queue
EVENT_DICT[3] = completion_queue.get(deadline=None)
# Fourth request -- read the response for our request
read_result = call_obj.read(tag='5:READ-TAG')
# Read off remaining events from queue
EVENT_DICT[4] = completion_queue.get(deadline=None)
EVENT_DICT[5] = completion_queue.get(deadline=None)
# We only expect 5 events (1 for each tag)
EVENT_DICT[6] = completion_queue.get(deadline=1)


for i in xrange(1, 6 + 1):
    print('Event %d' % (i,))
    print(EVENT_DICT[i])
    print('')
