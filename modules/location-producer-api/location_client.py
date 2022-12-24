import grpc

import location_pb2
import location_pb2_grpc

"""
Simulates user mobiles sending coordinates to gRPC
"""

print("Coordinates sending...")

channel = grpc.insecure_channel("127.0.0.1:5005")
stub = location_pb2_grpc.ItemServiceStub(channel)

location = location_pb2.LocationMessage(
    personId=300,
    latitude=-100,
    longitude=30
)

location_2 = location_pb2.LocationMessage(
    personId=400,
    latitude=-100,
    longitude=30
)

response_1 = stub.Create(location)
response_2 = stub.Create(location_2)


print("Coordinates sent...")
print(location, location_2)