import asyncio
import logging
import requests
from asyncua import Client

_logger = logging.getLogger('asyncua')

API_HOST = "localhost"
API_PORT = 8000
OPC_UA_HOST = "localhost"
OPC_UA_PORT = 4840

request_url = f"http://{API_HOST}:{API_PORT}/api/dm/v1/messages"
class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """
    async def datachange_notification(self, node, val, data):
        print("New data change event", node, val)
        id, message_type, start_time, status_code, machine_id = val.split(",")
        body = {
            "id": id,
            "message_type": message_type,
            "start_time": start_time,
            "status_code": status_code,
            "machine_id": machine_id
        }
        response = requests.post(url=request_url, json=body, headers={
            'Content-Type': "application/json"
        })
        print(response.json())

    def event_notification(self, event):
        print("New event", event)


async def main():
    url = f"opc.tcp://{OPC_UA_HOST}:{OPC_UA_PORT}/freeopcua/server/"
    async with Client(url=url) as client:
        _logger.info("Root node is: %r", client.nodes.root)
        _logger.info("Objects node is: %r", client.nodes.objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        _logger.info("Children of root are: %r", await client.nodes.root.get_children())

        uri = "http://examples.freeopcua.github.io"
        idx = await client.get_namespace_index(uri)
        _logger.info("index of our namespace is %s", idx)

        # Now getting a variable node using its browse path
        message_var = await client.nodes.objects.get_child(["1:MyXMLFolder", "1:MyXMLObject", "1:MyXMLVariable"])
        _logger.info("myvar is: %r", message_var)

        # subscribing to a variable node
        handler = SubHandler()
        sub = await client.create_subscription(10, handler)
        handle = await sub.subscribe_data_change(message_var)
        await asyncio.sleep(0.1)
        
        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
