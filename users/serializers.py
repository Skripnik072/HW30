from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from users.models import Payment, User,Subscription, Paymcourse


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username', 'phone', 'avatar', 'city']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

class PaymcourseSerializer(ModelSerializer):
    class Meta:
        model = Paymcourse
        fields = "__all__"
