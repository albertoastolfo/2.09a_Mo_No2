from email import message
import sys
import zmq
import logging

class NameSubscriber(object):
    def __init__(self,id):
        port = "6666"
        address = f'tcp://127.0.0.1:{port}'
        topicfilter = b'9999'

        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(address)
        logging.info(f'id {id} subscribing to {address}')

        self.socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
    
    def poll(self):
        if self.socket.poll(1):
            string = self.socket.recv()
            topic, message = string.split()
            #logging.info(message)
            return message.decode('UTF-8')
