from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Employee, Catalog, Product, ProductFilters
from .serializers import EmployeeSerializer, CatalogSerializer, ProductSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilters
