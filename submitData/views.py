"""
Представления реализуют RestAPI для добавления перевалов, получения и редактирование данных перевалов.

1.  - SubmitData добавляет новый перевал с вложенными данными (user, coords, images) (POST)
    - Возвращает список перевалов по email. Если email не указан, то возвращает ошибку 404 (GET)
2.  - PerevalReturnIdUpdate возвращает данные перевала по id. (GET)
    - Обновляет данные перевала по id, если статус 'new'. Обновляются поля, координаты, изображения. (PATCH)
"""
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PerevalAdded
from .serializers import PerevalAddedSerializer, PerevalInfoSerializer, PerevalUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SubmitData(APIView):
    # Описание get запроса на получение списка перевалов по email
    @swagger_auto_schema(
        operation_description="Получить список перевалов по email пользователя",
        manual_parameters=[
            openapi.Parameter(
                'user__email',
                openapi.IN_QUERY,
                description="Email пользователя, чьи перевалы нужно получить",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: PerevalInfoSerializer(many=True)}
    )

    def get(self, request):
        email = request.query_params.get('user__email')
        if not email:
            return Response({'error': 'Не указан параметр user__email'}, status=400)

        perevals = PerevalAdded.objects.filter(user__email=email)
        serializer = PerevalInfoSerializer(perevals, many=True)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        operation_description="Отправить новый перевал",
        request_body=PerevalAddedSerializer,
        responses={201: openapi.Response(description="Успешное создание", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                'message': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                'id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ))}
    )


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
    # Описание get запроса на получение информации о перевале по id
    @swagger_auto_schema(
        operation_description="Получить подробную информацию о перевале по ID",
        responses={200: PerevalInfoSerializer()}
    )

    # Возвращение информации по id
    def get(self, request, id):
        pereval = get_object_or_404(PerevalAdded, id=id)
        serializer = PerevalInfoSerializer(pereval)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Описание PATCH-запроса на частичное обновление перевала
    @swagger_auto_schema(
        operation_description="Обновить перевал по ID (если статус = 'new')",
        request_body=PerevalUpdateSerializer,
        responses={
            200: openapi.Response(description="Успешное обновление", schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'state': openapi.Schema(type=openapi.TYPE_INTEGER)}
            )),
            400: "Ошибка валидации или статус не 'new'"
        }
    )

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
        serializer = PerevalUpdateSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'state': 1}, status=status.HTTP_200_OK)
        # Ошибка валидации
        return Response({'state': 0, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)