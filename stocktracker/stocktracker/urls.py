from django.contrib import admin
from django.urls import include, path
from stocks import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", views.APIRoot.as_view(), name="api-root"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("stocks/", views.StockList.as_view(), name="stocks"),
    path("admin/", admin.site.urls, name="admin"),
]
