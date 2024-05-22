
from rest_framework import serializers
from .models import User, Expense, ExpenseShare

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'mobile']

class ExpenseShareSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()

    class Meta:
        model = ExpenseShare
        fields = ['user_id', 'share', 'percentage']

class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseShareSerializer(many=True)
    payer_id = serializers.UUIDField()

    class Meta:
        model = Expense
        fields = ['expense_id', 'payer_id', 'amount', 'expense_type', 'participants']

    def validate(self, data):
        participants = data.get('participants', [])
        total_amount = data.get('amount')
        expense_type = data.get('expense_type')

        if expense_type == 'EQUAL':
            if len(participants) > 0:
                equal_share = total_amount / len(participants)
                for participant in participants:
                    participant['share'] = equal_share
                    participant['percentage'] = None

        elif expense_type == 'EXACT':
            total_share = sum(p['share'] for p in participants)
            if total_share != total_amount:
                raise serializers.ValidationError("Total shares do not match the amount paid.")

        elif expense_type == 'PERCENT':
            total_percentage = sum(p['percentage'] for p in participants)
            if total_percentage != 100:
                raise serializers.ValidationError("Total percentages do not add up to 100.")
            for participant in participants:
                participant['share'] = (total_amount * participant['percentage']) / 100

        return data

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        expense = Expense.objects.create(**validated_data)
        for participant_data in participants_data:
            ExpenseShare.objects.create(expense_id=expense.expense_id, **participant_data)
        return expense
