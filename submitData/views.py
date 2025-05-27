"""
Представления реализуют RestAPI для добавления перевалов.

1.  - SubmitData добавляет новый перевал с вложенными данными (user, coords, images) (POST)
    - Возвращает список перевалов по email. Если email не указан, то возвращает ошибку 404 (GET)
2.  - PerevalReturnId возвращает данные перевала по id. (GET)
"""
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PerevalAdded
from .serializers import PerevalAddedSerializer, PerevalInfoSerializer, PerevalUpdateSerializer


class SubmitData(APIView):
    def get(self, request):
        email = request.query_params.get('user__email')
        if not email:
            return Response({'error': 'Не указан параметр user__email'}, status=400)

        perevals = PerevalAdded.objects.filter(user__email=email)
        serializer = PerevalInfoSerializer(perevals, many=True)
        return Response(serializer.data, status=200)


    def post(self, request):
        serializer = PerevalAddedSerializer(data=request.data)
        if serializer.is_valid():
            return self.handle_valid_data(serializer)
        return self.handle_invalid_data(serializer)

    def handle_valid_data(self, serializer):
        try:
            # Сохранение перевала, если данные валидны
            pereval = serializer.save()
            return Response({
                'status': 200,
                'message': None,
                'id': pereval.id
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': 500,
                'message': f'Ошибка при сохранении: {str(e)}',
                'id': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_invalid_data(self, serializer):
        # Возвращаем ошибку, если данные невалидны
        return Response({
            'status': 400,
            'message': 'Ошибка валидации',
            'errors': serializer.errors,
            'id': None
        }, status=status.HTTP_400_BAD_REQUEST)

class PerevalReturnIdUpdate(APIView):

    # Возвращение информации по id
    def get(self, request, id):
        pereval = get_object_or_404(PerevalAdded, id=id)
        serializer = PerevalInfoSerializer(pereval)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Обновление перевала
    def patch(self, request, id):
        # Возвращаем объект перевала по id
        pereval = get_object_or_404(PerevalAdded, id=id)

        if pereval.status != 'new':
            return Response({
                'state': 0,
                'message': 'Невозможно отредактировать запись. Для изменения записи ее статус должен быть "new".'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Проводим обновление
        serializer = PerevalReturnIdUpdate(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'state': 1}, status=status.HTTP_200_OK)
        # Ошибка валидации
        return Response({'state': 0, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)