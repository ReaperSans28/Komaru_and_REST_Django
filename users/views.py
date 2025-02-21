from rest_framework import viewsets, generics, filters

from users.models import Payments
from users.serializer import PaymentsSerializers, UserSerializer


class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializers
    queryset = Payments.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['paid_course', 'separately_paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
