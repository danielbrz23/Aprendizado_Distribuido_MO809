import grpc
import lab1_pb2 as pb2
import lab1_pb2_grpc as pb2_grpc
import ray
import random

ray.init()

@ray.remote
class Actor:
    def __init__(self, message, client_id):
        self.message = message
        self.client_id = client_id
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = pb2_grpc.MLStub(self.channel)

    def send