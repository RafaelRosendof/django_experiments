from celery import shared_task
from .models.client import Client, ClientAddress, ClientPhone


@shared_task
def create_client_task(client_data):
    """
    Task to create a client along with all data, this is just for practice the use of celery
    """
    phone_data = client_data.pop('phones', [])
    address_data = client_data.pop('addresses', [])

    client = Client.objects.create(**client_data)

    for phone in phone_data:
        ClientPhone.objects.create(client=client, **phone)

    for address in address_data:
        ClientAddress.objects.create(client=client, **address)

    return f'Client {client.name} created with ID {client.id}'