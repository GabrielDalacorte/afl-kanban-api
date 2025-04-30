from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.kanban.models import Board, Column, Card
from apps.kanban.api.serializers import BoardSerializer, ColumnSerializer, CardSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

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
        self.perform_destroy(instance)
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

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.column.name.lower() == "produção":
            if instance.status != "done":
                instance.status = "done"
                instance.save(update_fields=["status"])