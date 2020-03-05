import os
import sys
import time
from concurrent import futures

import createnotification
import createnotification_pb2
import createnotification_pb2_grpc
import grpc


class CreateNotificationServicer(createnotification_pb2_grpc.CreateNotificationServicer):

    def create_notification(self, request, context):
        response = createnotification_pb2.ResponseData()
        response.successfully, response.message_id = createnotification.create_notification(
            request.template,
            request.microservice_id,
            request.user_id,
            request.content,
        )
        return response


def serve():
    # создаем сервер
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

    # прикреплям хандлер
    createnotification_pb2_grpc.add_CreateNotificationServicer_to_server(
        CreateNotificationServicer(),
        server)

    # запускаемся на порту 40535
    print('Starting server on port 40535.')
    server.add_insecure_port('[::]:40535')
    server.start()

    # работаем год либо до прерывания с клавиатуры
    try:
        while True:
            time.sleep(364 * 24 * 3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
