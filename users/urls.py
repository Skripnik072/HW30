from django.urls import path

from users.apps import UsersConfig
from users.views import (
    PaymentListApiView,
    PaymentCreateApiView,
    PaymentUpdateApiView,
    PaymentRetrieveApiView,
    PaymentDestroyApiView
)

app_name = UsersConfig.name


urlpatterns = [
    path("payments/", PaymentListApiView.as_view(), name="payments_list"),
    path("payments/<int:pk>/", PaymentRetrieveApiView.as_view(), name="payments_retrieve"),
    path("payments/create/", PaymentCreateApiView.as_view(), name="payments_create"),
    path(
        "payments/<int:pk>/delete/",
        PaymentDestroyApiView.as_view(),
        name="payments_delete",
    ),
    path(
        "payments/<int:pk>/update/", PaymentUpdateApiView.as_view(), name="payments_update"
    ),
]