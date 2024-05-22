# expenses/views.py

from rest_framework import viewsets
from .models import User, Expense
from .serializers import UserSerializer, ExpenseSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
