from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, CatalogViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'catalogs', CatalogViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
