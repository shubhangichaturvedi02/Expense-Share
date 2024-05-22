
import uuid
from django.db import models
from django.core.exceptions import ValidationError


def generate_uuid():
    return uuid.uuid4()

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = [
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENT', 'Percent'),
    ]

    expense_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payer_id = models.UUIDField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=7, choices=EXPENSE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.payer_id} paid {self.amount}"

    def save(self, *args, **kwargs):
        if not self.expense_id:
            self.expense_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        
        # Validate number of participants
        if self.participants.count() > 1000:
            raise ValidationError('Maximum number of participants exceeded (1000).')

        # Validate maximum amount
        max_amount = 10000000  # INR 1,00,00,000
        if self.amount > max_amount:
            raise ValidationError(f'Maximum amount exceeded (INR {max_amount}).')


class ExpenseShare(models.Model):
    expense_id = models.UUIDField()
    user_id = models.UUIDField()
    share = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user_id} owes {self.share} for {self.expense_id}"
