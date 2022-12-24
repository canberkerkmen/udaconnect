import json
import os
import logging

from concurrent import futures
from kafka import KafkaProducer

import grpc

import location_pb2_grpc
import location_pb2

kafka_url = os.environ["KAFKA_URL"]
kafka_topic = os.environ["KAFKA_TOPIC"]

logging.info('connecting to kafka ', kafka_url)
print('p_connecting to kafka ', kafka_url)
logging.info('connecting to kafka topic ', kafka_topic)
print('p_connecting to kafka topic ', kafka_topic)

producer = KafkaProducer(bootstrap_servers=kafka_url)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):

    def Create(self, request, context):
        request_value = {
            'personId': int(request.personId),
            'latitude': int(request.latitude),
            'longitude': int(request.longitude)
        }

        logging.info('processing entity ', request_value)

        user_encode_data = json.dumps(request_value, indent=2).encode('utf-8')
        producer.send(kafka_topic, user_encode_data)
        return location_pb2.LocationMessage(**request_value)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

logging.info('starting on port 5005')
server.add_insecure_port('[::]:5005')
server.start()
server.wait_for_termination()