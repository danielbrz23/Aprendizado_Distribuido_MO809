import grpc
import ping_pong_pb2 as pb2
import ping_pong_pb2_grpc as pb2_grpc
import time
import ray

@ray.remote
def client_process(mensagem, client_id):
    channel = grpc.insecure_channel("localhost:50051")
    stub = pb2_grpc.PingPongStub(channel)

    message = pb2.Ping(mensagem=mensagem)
    response = stub.GetServerResponse(message)

    return response.mensagem  # Assuming the response has a 'mensagem' attribute

if __name__ == '__main__':
    client_id = 1  # Example client ID
    mensagens = ['Ping!'] * 10  # Create a list of 10 identical messages
    ids       = list(range(10))

    results = ray.get([client_process.remote(f'{message} - {client_id}', client_id) for message, client_id in zip(mensagens, ids)])
    print(results)