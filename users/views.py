from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.generics import (ListAPIView, CreateAPIView,
    RetrieveAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from users.models import Payment, User, Subscription,Paymcourse
from materials.models import Course
from users.serializers import (PaymentSerializer, UserSerializer,
    SubscriptionSerializer,PaymcourseSerializer)
from materials.serializers import CourseSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class UserListApiView(ListAPIView):
    '''Дженерик для просмотра списка пользователей'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UserCreateApiView(CreateAPIView):
    '''Дженерик для создания пользователя'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserRetrieveApiView(RetrieveAPIView):
    '''Дженерик для получения пользователя'''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(UpdateAPIView):
    '''Дженерик для обновления пользователя'''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyApiView(DestroyAPIView):
    '''Дженерик для удаления пользователя'''
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListApiView(ListAPIView):
    '''Дженерик для просмотра платежей'''
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method",)
    ordering_fields = ["date",]


class PaymentCreateApiView(CreateAPIView):
    '''Дженерик для создания платежа'''
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentRetrieveApiView(RetrieveAPIView):
    '''Дженерик для получения платежа'''
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateApiView(UpdateAPIView):
    '''Дженерик для обоновления платежа'''
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyApiView(DestroyAPIView):
    '''Дженерик для удаления платежа'''
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class SubscriptionApiView(APIView):
    '''Дженерик для работы с подписками на курс'''
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

class PaymcourseCreateApiView(CreateAPIView):
    '''Дженерик для создания оплаты за курс'''
    queryset = Paymcourse.objects.all()
    serializer_class = PaymcourseSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_price(payment.amount)
        session_id, payment_link = create_stripe_session(price)
        product = create_stripe_product(payment.course)
        payment_course = product
        payment_session_id = session_id
        payment_link = payment_link
        payment.save()
