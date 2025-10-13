from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseCreateApiView, CourseDestroyApiView,
                             CourseListApiView, CourseRetrieveApiView,
                             CourseUpdateApiView, LessonViewSet)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", LessonViewSet)

urlpatterns = [
    path("courses/", CourseListApiView.as_view(), name="courses_list"),
    path("courses/<int:pk>/", CourseRetrieveApiView.as_view(), name="courses_retrieve"),
    path("courses/create/", CourseCreateApiView.as_view(), name="courses_create"),
    path(
        "courses/<int:pk>/delete/",
        CourseDestroyApiView.as_view(),
        name="courses_delete",
    ),
    path(
        "courses/<int:pk>/update/", CourseUpdateApiView.as_view(), name="courses_update"
    ),
]

urlpatterns += router.urls
