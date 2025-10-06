
from rest_framework import viewsets
from crudEx.models.client import Client, ClientAddress, ClientPhone
from crudEx.serializers import ClientSerializer, ClientAddressSerializer, ClientPhoneSerializer
from crudEx.models.employee import Employee, EmployeeAddress, EmployeePhone
from crudEx.serializers import EmployeeSerializer, EmployeeAddressSerializer, EmployeePhoneSerializer
from crudEx.models.product import Product
from crudEx.serializers import ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import time
from .tasks import create_client_task
from rest_framework.permissions import IsAuthenticated


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'] , url_path='filter-by-mail')
    def filter_by_mail(self, request):

        email = request.query_params.get('email', None)
        if email is not None:
            clients = Client.objects.filter(email=email)
            if clients.exists():
                serializer = self.get_serializer(clients, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail": "No clients found with the provided email."}, status=404)
        else:
            return Response({"detail": "Email query parameter is required."}, status=400)
        
    '''
    {
    "name": "Innovate Tech Brasil (Updated Name)",
    "email": "contato.novo@innovatebr.com",
    "phones": [
        {
            "phone_number": "+55 84 98888-2002"
        }
    ],
    "addresses": [
        {
            "address_line": "Av. Engenheiro Roberto Freire, 2100",
            "city": "Natal",
            "postal_code": "59082-902"
        }
    ]
}
    '''

    #this method, is just for adding a client, but it gonna have a timeout just to practice the use of celery
    @action(detail=False, methods=['post'] , url_path='add-client-with-delay')
    def add_client_with_delay(self, request):

        client_data = request.data

        create_client_task.apply_async(args=[client_data], countdown=5)

        return Response({"detail": "Client creation task has been scheduled and will be processed shortly."}, status=202)

        



class ClientAddressViewSet(viewsets.ModelViewSet):
    queryset = ClientAddress.objects.all()
    serializer_class = ClientAddressSerializer
    permission_classes = [IsAuthenticated]


class ClientPhoneViewSet(viewsets.ModelViewSet):
    queryset = ClientPhone.objects.all()
    serializer_class = ClientPhoneSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeAddressViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAddress.objects.all()
    serializer_class = EmployeeAddressSerializer

class EmployeePhoneViewSet(viewsets.ModelViewSet):
    queryset = EmployeePhone.objects.all()
    serializer_class = EmployeePhoneSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['put'] , url_path='update-prices')
    def bulk_update_prices(self, request):

        update = request.data.get('update', None)

        if update is not None:
            product_id = update.get('id', None)
            new_price = update.get('price', None)

            if product_id is not None and new_price is not None:
                try:
                    product = Product.objects.get(id=product_id)
                    product.price = new_price
                    product.save()
                    serializer = self.get_serializer(product)
                    return Response(serializer.data)
                
                except Product.DoesNotExist:
                    return Response({"detail": "Product not found."}, status=404)
        

