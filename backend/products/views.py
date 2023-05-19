from rest_framework import viewsets

from .models import Product
from api.mixins import StaffEditorPermissionMixin, UserQueryMixin
from .serializers import ProductSerializer


class ProductViewSet(UserQueryMixin, StaffEditorPermissionMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
