from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    LessonDetailSerializer,
)
from users.permissions import IsModer, IsOwner


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LessonDetailSerializer
        return LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


    def get_permissions(self):
        if self.action in "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class CourseListApiView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseCreateApiView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class CourseRetrieveApiView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class CourseUpdateApiView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class CourseDestroyApiView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwner, ~IsModer]
