from django.contrib.auth.models import Group, User
from rest_framework import generics, permissions, viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from stocks.models import Stock
from stocks.serializers import GroupSerializer, StockSerializer, UserSerializer


# User and Group views for simple auth purposes
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


class StockList(ListModelMixin, CreateModelMixin, generics.GenericAPIView):
    """
    List all stocks, or create a new one to keep track of.
    """

    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
