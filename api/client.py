import createnotification_pb2
import createnotification_pb2_grpc
import grpc


class ClientCreateNotification:
    """
    Class for calling GRPC API methods
    """

    def __init__(self):
        # открываем канал
        self.channel = grpc.insecure_channel('localhost:40535')
        self.stub = createnotification_pb2_grpc.CreateNotificationStub(self.channel)

    def client_registration_email_confirmation(self, data):
        print('client_registration_email_confirmation: ', end='')
        content={
            'username': data['username'],
            'email': data['email'],
            'link': data['link'],
        }
        to_data = createnotification_pb2.RequestData(
            template='client_registration_email_confirmation',
            microservice_id=data['microservice_id'],
            user_id=data['user_id'],
            content=content,
        )
        response = self.stub.create_notification(to_data)
        print('{}, {}'.format(response.successfully, response.message_id))

    def client_forgot_password_email(self, data):
        print('client_forgot_password_email: ', end='')
        content={
            'username': data['username'],
            'email': data['email'],
            'link': data['link'],
        }
        to_data = createnotification_pb2.RequestData(
            template='client_forgot_password_email',
            microservice_id=data['microservice_id'],
            user_id=data['user_id'],
            content=content,
        )
        response = self.stub.create_notification(to_data)
        print('{}, {}'.format(response.successfully, response.message_id))


    def client_invoice_email(self, data):
        print('client_invoice_email: ', end='')
        content={
            'username': data['username'],
            'email': data['email'],
            'invoice_id': data['invoice_id'],
            'invoice_number': data['invoice_number'],
            'invoice_date': data['invoice_date'],
            'reporting_period': data['reporting_period'],
            'link': data['link'],
        }
        to_data = createnotification_pb2.RequestData(
            template='client_invoice_email',
            microservice_id=data['microservice_id'],
            user_id=data['user_id'],
            content=content,
        )
        response = self.stub.create_notification(to_data)
        print('{}, {}'.format(response.successfully, response.message_id))

    def client_account_successfully_deleted_email_sms(self, data):
        print('client_account_successfully_deleted_email_sms: ', end='')
        content={
            'username': data['username'],
            'email': data['email'],
            'phone': data['phone'],
        }
        to_data = createnotification_pb2.RequestData(
            template='client_account_successfully_deleted_email_sms',
            microservice_id=data['microservice_id'],
            user_id=data['user_id'],
            content=content,
        )
        response = self.stub.create_notification(to_data)
        print('{}, {}'.format(response.successfully, response.message_id))

    def client_registration_sms_confirmation(self, data):
        print('client_registration_sms_confirmation: ', end='')
        content={
            'phone': data['phone'],
            'phone_key': data['phone_key'],
        }
        to_data = createnotification_pb2.RequestData(
            template='client_registration_sms_confirmation',
            microservice_id=data['microservice_id'],
            user_id=data['user_id'],
            content=content,
        )
        response = self.stub.create_notification(to_data)
        print('{}, {}'.format(response.successfully, response.message_id))


    def client_forgot_password_sms(self, data):
        print('client_forgot_password_sms: ', end='')
        content={
            'phone': data['phone'],
            'phone_key': data['phone_key'],
        }
        to_data = createnotification_pb2.RequestData(
            template='client_forgot_password_sms',
            microservice_id=data['microservice_id'],
            user_id=data['user_id'],
            content=content,
        )
        response = self.stub.create_notification(to_data)
        print('{}, {}'.format(response.successfully, response.message_id))


if __name__ == '__main__':
    test_data = {
        'microservice_id': 17, # id микросервиса который отправляет уведомление
        'user_id': 133,
        'username': 'Bob',
        'email': 'recipient@mail.com',
        'link': 'http://site.com/registration/abcdfegkl/',
        'invoice_id': '222',
        'invoice_number': '333',
        'invoice_date': '1 февраля 2020',
        'reporting_period': 'с 1 января 2020 по 31 января 2020',
        'phone': '380997777777',
        'phone_key': 'abc258',
    }
    client = ClientCreateNotification()
    client.client_registration_email_confirmation(test_data)
    client.client_forgot_password_email(test_data)
    client.client_invoice_email(test_data)
    # client.client_account_successfully_deleted_email_sms(test_data)
    # client.client_registration_sms_confirmation(test_data)
    # client.client_forgot_password_sms(test_data)
