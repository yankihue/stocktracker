from rest_framework import generics, permissions
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from stocks.models import Stock
from stocks.serializers import StockSerializer


class APIRoot(generics.GenericAPIView):
    """
    API entry point.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        return Response(
            {
                "stocks": reverse("stocks", request=request, format=format),
            }
        )


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
