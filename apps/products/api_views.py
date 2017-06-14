from .models import Products, ACTIVE_STATUS
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from .serializers import ProductListSerializer, ProductDetailSerializer
from rest_framework.response import Response
from rest_framework import status

class ProductList(mixins.ListModelMixin,generics.GenericAPIView):
    #limit 8 softwares
    queryset = Products.objects.filter(in_homepage=True)[:8]
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny,]


    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)

class ProductListAll(mixins.ListModelMixin, generics.GenericAPIView):
    """all product"""
    queryset = Products.objects.filter(status=ACTIVE_STATUS).filter(in_homepage=True)
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny,]


    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)


class ProductDetail(generics.GenericAPIView):
    """software detail"""
    permission_classes = [AllowAny,]
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
            result = generics.get_object_or_404(Products, uuid=id)
        except Exception as e:
            print(e)
            return Response("error", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(result,data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
