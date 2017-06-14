from .models import Products
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from .serializers import ProductListSerializer

class ProductList(mixins.ListModelMixin,generics.GenericAPIView):
    #limit 8 softwares
    queryset = Products.objects.filter(in_homepage=True)[:8]
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny,]


    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)
