from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from materials.models import Course, Lesson
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    LessonDetailSerializer,
)
from materials.tasks import send_update
from users.permissions import IsModer, IsOwner
from materials.paginations import CustomPagination


class LessonViewSet(ModelViewSet):
    '''Вьсет для операций CRUD по урокам'''
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

    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]


class CourseListApiView(ListAPIView):
    '''Дженерик для вывода списка курсов'''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CustomPagination]


class CourseCreateApiView(CreateAPIView):
    '''Дженерик для создания курса'''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny,]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class CourseRetrieveApiView(RetrieveAPIView):
    """Дженерик для получения курса из модели"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny,]


class CourseUpdateApiView(UpdateAPIView):
    '''Дженерик для обновления курса'''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny,]

    def perform_update(self, serializer):
        course = serializer.save()
        result = send_update(course_id=course.id).delay(course.id)
        return result


class CourseDestroyApiView(DestroyAPIView):
    '''Дженерик для удаления курса'''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny,]
