import grpc
from concurrent import futures
import time
import numpy as np

import lab1_pb2_grpc as pb2_grpc
import lab1_pb2 as pb2

from sklearn.neighbors import KNeighborsClassifier

class Server(pb2_grpc.MLServicer):

    def __init__(self):
        self.model = KNeighborsClassifier()

    def train(self, request, context):
        X = []
        y = []

        dataset = request.dataset

        for sample in dataset.samples:
            X.append(sample.features)
            y.append(sample.label)

        X = np.array(X)
        y = np.array(y)

        self.model.fit(X=X, y=y)
        accuracy = self.model.score(X, y)

        return pb2.FitResponse(accuracy=accuracy)

    def eval(self, request, context):
        features = np.array(request.features)
        if len(features.shape) < 2:
            features = features.reshape(1,-1)
        pred = self.model.predict(features)
        return pb2.PredictResponse(predicted_label=int(pred[0]))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MLServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()