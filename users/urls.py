from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import (
    PaymentListApiView,
    PaymentCreateApiView,
    PaymentUpdateApiView,
    PaymentRetrieveApiView,
    PaymentDestroyApiView,
    UserListApiView,
    UserCreateApiView,
    UserUpdateApiView,
    UserRetrieveApiView,
    UserDestroyApiView
)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateApiView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
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
    path("users/", UserListApiView.as_view(), name="users_list"),
    path("users/<int:pk>/", UserRetrieveApiView.as_view(), name="users_retrieve"),
    path("users/create/", UserCreateApiView.as_view(), name="users_create"),
    path(
        "users/<int:pk>/delete/",
        UserDestroyApiView.as_view(),
        name="users_delete",
    ),
    path(
        "users/<int:pk>/update/", UserUpdateApiView.as_view(), name="users_update"
    ),
]