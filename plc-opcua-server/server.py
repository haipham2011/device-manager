import asyncio
import copy
import logging
from datetime import datetime
import time
from math import sin
import random


from asyncua import ua, uamethod, Server


class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


# method to be exposed through server
def func(parent, variant):
    ret = False
    if variant.Value % 2 == 0:
        ret = True
    return [ua.Variant(ret, ua.VariantType.Boolean)]


async def main():
    # now setup our server
    server = Server()
    await server.init()
    server.disable_clock()  #for debuging
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    server.set_server_name("FreeOpcUa Example Server")
    # set all possible endpoint policies for clients to connect through
    server.set_security_policy([
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ua.SecurityPolicyType.Basic256Sha256_Sign])
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)                   

    # import some nodes from xml
    await server.import_xml("message_nodes.xml")

    # creating a default event object
    # The event object automatically will have members for all events properties
    # you probably want to create a custom event type, see other examples
    myevgen = await server.get_event_generator()
    myevgen.event.Severity = 300

    # starting!
    async with server:
        print("Available loggers are: ", logging.Logger.manager.loggerDict.keys())
        root_path = await server.nodes.objects.get_child(["1:MyXMLFolder", "1:MyXMLObject", "1:MyXMLVariable"])

        message_id = 0
        while True:
            await asyncio.sleep(5)
            # id , message_type , start_time, status_code, machine_id
            message_type = random.choice(["error", "info", "warning"])
            now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
            start_time = now
            status_code = random.choice([101, 201, 301])
            machine_id = random.choice([1, 2, 3])
            await server.write_attribute_value(root_path.nodeid, ua.DataValue(f"{message_id},{message_type},{start_time},{status_code},{machine_id}"))
            message_id += 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
