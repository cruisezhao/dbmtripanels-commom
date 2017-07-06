from .models import ProductApps, ACTIVE_STATUS, Products
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ProductAppsListSerializer, ProductAppsDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from .filters4api import ProductAppsFilter4API
from rest_framework.filters import SearchFilter,DjangoFilterBackend

class ProductList(mixins.ListModelMixin,generics.GenericAPIView):
    #limit 8 softwares
    queryset = ProductApps.objects.all()[:8]
    serializer_class = ProductAppsListSerializer
    permission_classes = [AllowAny,]


    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)

class ProductListAll(mixins.ListModelMixin, generics.GenericAPIView):
    """all product"""
    queryset = ProductApps.objects.all()
    serializer_class = ProductAppsListSerializer
    permission_classes = [AllowAny,]
    filter_backends = (SearchFilter,)
    search_fields = ('app_name', 'summary', 'features', 'description')


    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)


class ProductDetail(generics.GenericAPIView):
    """software detail"""
    permission_classes = [AllowAny,]
    serializer_class = ProductAppsDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id', None)
            p = generics.get_object_or_404(Products, uuid=id)
            result = generics.get_object_or_404(ProductApps, product=p)
        except Exception as e:
            print(e)
            return Response("error", status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(result,data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class Istrialed(APIView):
    """whether the logined person can trial or not"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if allowed_order(request):
            return Response('true',status = status.HTTP_200_OK)
        else:
            return Response('false', status = status.HTTP_403_FORBIDDEN)