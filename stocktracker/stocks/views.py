import requests
from django.contrib.auth.models import Group, User
from rest_framework import generics, permissions, viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from stocks.models import Stock
from stocks.serializers import GroupSerializer, StockSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# class StocksViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows stocks to be viewed.
#     """

#     queryset = Stock.objects.all()
#     serializer_class = StockSerializer
#     permission_classes = [permissions.IsAuthenticated]


class StockList(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    """
    List all snippets, or create a new snippet.
    """

    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
