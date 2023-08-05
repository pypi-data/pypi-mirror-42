# The Python Banyan Framework
![](https://github.com/MrYsLab/python_banyan/blob/master/images/BanyanTree.png)


The Python Banyan Framework is a lightweight, reactive framework used to
create flexible, non-blocking, event driven, asynchronous applications.
It was designed primarily to aid in the implementation of real-time physical computing applications
 for devices such as
 the Raspberry Pi, ESP8266,  and Arduino,
but may easily be applied to projects outside of the physical programming domain.

It is being used by [Palace Games](https://www.raspberrypi.org/blog/raspberry-pi-escape-room/)
to concurrently monitor hundreds of real-time sensors and actuators.

* Based on a network connected Publish/Subscribe model,  Banyan components publish 
user defined protocol messages in the form of Python dictionaries.
* A Banyan protocol message may contain Numpy data.
* Applications may reside on a single computer or be distributed across 
multiple computers without having to change source code.
* Compatible Banyan Frameworks are available for [JavaScript](https://github.com/MrYsLab/js-banyan), [Ruby](https://github.com/MrYsLab/rb_banyan), and
[Java](https://github.com/MrYsLab/javabanyan). Components written in any of these languages can interact with components of a differing language without modification.
* Runs on Python 2 or Python 3 (recommended).

New Features Introduced in 3.0
* An MQTT Gateway to interconnect MQTT and Banyan networks so that data may be shared.
* A new "learn by example" [User's Guide](https://mryslab.github.io/python_banyan/) is provided.
* A component launcher that will allows you to launch Banyan components on a single 
computer or multiple computers, all from a single command.

Use pip to install. View the full [installation instructions](https://mryslab.github.io/python_banyan/install/#installing-python-banyan_1)

A Sample Banyan Component:

```
import sys
from python_banyan.banyan_base import BanyanBase


class EchoServer(BanyanBase):
    """
    This class is a simple Banyan echo server
    """
    def __init__(self, ):

        # initialize the parent
        super(EchoServer, self).__init__(process_name='EchoServer')

        # subscribe to receive 'echo' messages from the client
        self.set_subscriber_topic('echo')

        # wait for messages to arrive
        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)

    def incoming_message_processing(self, topic, payload):
        """
        Process incoming messages from the client
        :param topic: message topic
        :param payload: message payload
        """
        # republish the message with a topic of reply
        self.publish_payload(payload, 'reply')
        
        # extract the message number from the payload
        print('Message number:', payload['message_number'])

```

This project was developed with [Pycharm](https://www.jetbrains.com/pycharm/) ![logo](https://github.com/MrYsLab/python_banyan/blob/master/images/icon_PyCharm.png)
