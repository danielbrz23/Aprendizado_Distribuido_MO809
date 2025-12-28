import grpc
import lab1_pb2 as pb2
import lab1_pb2_grpc as pb2_grpc
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
import time

class ClientGRPC(object):

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051
        self.channel = grpc.insecure_channel(f'{self.host}:{self.server_port}')
        self.stub = pb2_grpc.MLStub(self.channel)

    def Fit(self, X, y):
        dataset = pb2.Dataset()

        for features, label in zip(X,y):
            sample = pb2.Sample(
                features = features.tolist(),
                label = int(label)
            )
            dataset.samples.append(sample)

        request = pb2.FitRequest(dataset=dataset)
        return self.stub.train(request)
    
    def Predict(self, X):
        request = pb2.PredictRequest(features=X.tolist())
        return self.stub.eval(request)

if __name__ == '__main__':
    client = ClientGRPC()

    iris = load_iris()

    X = iris.data
    y = iris.target

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

        # ===== Treinamento =====
    tempo = time.time()
    print("Cliente -> Enviando dados para treino")
    resposta_treino = client.Fit(X_train, y_train)
    print(f"Servidor -> Acurácia de treino: {resposta_treino.accuracy}")
    print(f"Duração treino RPC: {time.time() - tempo}")
    print("--------------------------------")

    # ===== Predição =====
    amostra = X_val[0]
    classe_real = y_val[0]

    tempo = time.time()
    print("Cliente -> Enviando amostra para predição")
    resposta_predicao = client.Predict(amostra)
    print(f"Servidor -> Classe predita: {resposta_predicao.predicted_label}")
    print(f"Classe real: {classe_real}")
    print(f"Duração predição RPC: {time.time() - tempo}")
    print("--------------------------------")