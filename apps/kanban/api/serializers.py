from rest_framework import serializers
from apps.kanban.models import Board, Column, Card
from datetime import date

class CardSerializer(serializers.ModelSerializer):
    assignee_email = serializers.EmailField(source='assignee.email', read_only=True)
    delivery_date = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = Card
        fields = ['id', 'column', 'delivery_date', 'status', 'assignee', 'assignee_email', 'created_at']
        read_only_fields = ['id', 'created_at', 'assignee_email']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        delivery_date_obj = instance.delivery_date
        today = date.today()
        if (
            delivery_date_obj
            and delivery_date_obj < today
            and instance.status != 'done'
        ):
            data['status'] = 'late'
        elif instance.status != 'done':
            data['status'] = 'on_time'
        return data
    
class ColumnSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    class Meta:
        model = Column
        fields = ['id', 'board', 'name', 'order', 'cards']
        read_only_fields = ['id', 'cards']

class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'created_at', 'owner', 'owner_email', 'columns', 'active']
        read_only_fields = ['id', 'created_at', 'owner', 'owner_email', 'columns']