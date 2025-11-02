from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from users.models import Payment, User, Subscription
from materials.models import Course
from users.serializers import PaymentSerializer, UserSerializer, SubscriptionSerializer
from materials.serializers import CourseSerializer


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListApiView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method",)
    ordering_fields = ["date",]


class PaymentCreateApiView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentRetrieveApiView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateApiView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyApiView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class SubscriptionApiView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        ''' получаем пользователя '''
        user = self.request.user
        '''получаем id курса'''
        course_id = self.request.data['course_id']
        ''' получаем объект курса из базы'''
        course = get_object_or_404(Course, id=course_id)
        '''получаем объекты подписок по текущему пользователю и курсу'''
        subs_item = Subscription.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
        ''' возвращаем ответ в API '''
        return Response({"message": message})

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)
