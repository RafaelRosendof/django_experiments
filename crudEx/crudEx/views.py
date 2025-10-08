
from rest_framework import viewsets
from crudEx.models.client import Client, ClientAddress, ClientPhone
from crudEx.serializers import ClientSerializer, ClientAddressSerializer, ClientPhoneSerializer, ProductCategorySerializer
from crudEx.models.employee import Employee, EmployeeAddress, EmployeePhone
from crudEx.serializers import EmployeeSerializer, EmployeeAddressSerializer, EmployeePhoneSerializer
from crudEx.models.product import Product, ProductCategory
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
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'] , url_path='register-list-of-employees')
    def register_list_employees(self , request):
        employees = request.data

        if employees is not None and isinstance(employees, list):
            created_emps = []

            for i in employees:
                serializer = self.get_serializer(data=i)
                if serializer.is_valid():
                    serializer.save()
                    created_emps.append(serializer.data)
                else:
                    return Response(serializer.errors, status=400)

            return Response({"created_employees": created_emps}, status=201)

    #TODO add a method to reset the password of an employee django-reset-passwordreset method

    #@action(detail=True, methods=['post'] , url_path='reset-password')



class EmployeeAddressViewSet(viewsets.ModelViewSet):
    queryset = EmployeeAddress.objects.all()
    serializer_class = EmployeeAddressSerializer

class EmployeePhoneViewSet(viewsets.ModelViewSet):
    queryset = EmployeePhone.objects.all()
    serializer_class = EmployeePhoneSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'] , url_path='filter-by-price-range')
    def filter_by_price_range(self, request):

        min_price = request.query.params.get('min_price', None)
        max_price = request.query.params.get('max_price', None)

        if min_price is not None and max_price is not None:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
            except ValueError:
                return Response({"detail": "Invalid price values provided."}, status=400)

            products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
            if products.exists():
                serializer = self.get_serializer(products, many=True)
                return Response(serializer.data)
            else:
                return Response({"detail": "No products found in the specified price range."}, status=404)
            
    @action(detail=True , methods=['patch'] , url_path="updatePrice")
    def update_price(self , request , pk=None):

        #product_id = request.data.get("id", None)
        #product_id = request.parser_context['kwargs'].get('pk', None)
        product = self.get_object()
        new_price = request.data.get("price", None)

        if product and new_price is not None:
            try:
                new_price = float(new_price)
            except ValueError:
                return Response({"detail": "Invalid price value provided."}, status=400)

            product.price = new_price
            product.save(update_fields=['price'])
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        else:
            return Response({"detail": "Product ID and new price are required."}, status=400)

    def get_queryset(self):

        queryset = Product.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset


    @action(detail=False , methods=['get'] , url_path="get-by-name")
    def getByName(self , request , pk=None):
        
        name_product = request.query_params.get('name', None)
        if name_product is not None:
            product = Product.objects.filter(name=name_product).first()
            if product:
                serializer = self.get_serializer(product)
                return Response(serializer.data)
            else:
                return Response({"detail": "No product found with the provided name."}, status=404)
        else:
            return Response({"detail": "Name query parameter is required."}, status=400)


    @action(detail=False, methods=['post'] , url_path="add-multiple-products")
    def add_multiple_products(self , request):

        #products_data = request.data.get("products", None)
        products_data = request.data
        if products_data is not None and isinstance(products_data, list):
            created_prods = []

            for i in products_data:
                serializer = self.get_serializer(data=i)
                if serializer.is_valid():
                    serializer.save()
                    created_prods.append(serializer.data)
                else:
                    return Response(serializer.errors, status=400)

            return Response({"created_products": created_prods}, status=201)
        else:
            return Response({"detail": "Products data must be provided as a list."}, status=400)
        

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
        

