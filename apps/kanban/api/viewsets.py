from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.kanban.models import Board, Column, Card
from apps.kanban.api.serializers import BoardSerializer, ColumnSerializer, CardSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.db import models

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            active=True
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save(update_fields=["active"])
        return Response({"detail": "Board deletado com sucesso."}, status=status.HTTP_204_NO_CONTENT)
    
class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Column.objects.filter(board__owner=self.request.user)
        board_id = self.request.query_params.get('board')
        if board_id:
            queryset = queryset.filter(board_id=board_id)
        return queryset
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_order = request.data.get('order')
        if new_order is not None:
            try:
                new_order = int(new_order)
            except ValueError:
                return Response({"detail": "Order inválido."}, status=status.HTTP_400_BAD_REQUEST)

            if instance.order != new_order:
                other_column = Column.objects.filter(
                    board=instance.board,
                    order=new_order
                ).exclude(id=instance.id).first()
                if other_column:
                    other_column.order = instance.order
                    other_column.save(update_fields=["order"])
        return super().partial_update(request, *args, **kwargs)

class CardViewSet(viewsets.ModelViewSet):   
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Card.objects.filter(column__board__owner=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "done":
            raise ValidationError({"detail": "Não é possível mover um card com status 'Concluído'."})
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        column = serializer.validated_data['column']
        Card.objects.filter(column=column).update(order=models.F('order') + 1)
        serializer.save(
            assignee=self.request.user,
            status="on_time",
            order=1
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.column.name.lower() == "produção":
            if instance.status != "done":
                instance.status = "done"
                instance.save(update_fields=["status"])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Card deletado com sucesso."}, status=status.HTTP_204_NO_CONTENT)