from rest_framework.serializers import ModelSerializer

from users.models import Payments, User, Payment
from rest_framework import serializers


class PaymentsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
