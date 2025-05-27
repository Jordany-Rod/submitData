"""
Сериализаторы преобразуют данные моделей в формат, удобный для REST API,
и обратно — для сохранения в базу данных.

1. UserPassSerializer - сериализует пользователя, создаёт нового при необходимости (по email).
2. CoordPassSerializer - сериализует координаты перевала.
3. PerevalImagesSerializer - сериализует изображения перевала (название и ссылка).
4. PerevalAddedSerializer - сериализует перевал с вложенными данными (user, coords, images),
  создаёт связанные объекты.
"""

from .models import *
from rest_framework import serializers

class UserPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPass
        fields = ['email', 'fam', 'name', 'otc', 'phone']

    def create(self, validated_data):
        # Пытаемся найти пользователя по email
        user, created = UserPass.objects.get_or_create(
            email=validated_data['email'],
            defaults={
                'fam': validated_data.get('fam', ''),
                'name': validated_data.get('name', ''),
                'otc': validated_data.get('otc', ''),
                'phone': validated_data.get('phone', ''),
            }
        )
        return user

class CoordPassSerializer(serializers.ModelSerializer):
   class Meta:
       model = CoordPass
       fields = '__all__'

class PerevalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalImages
        fields = ['title', 'image_url']

class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UserPassSerializer()
    coords = CoordPassSerializer()
    images = PerevalImagesSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
            'user', 'coords',
            'level_winter', 'level_summer', 'level_autumn', 'level_spring',
            'images'
        ]

    def create(self, validated_data):
        # Извлекаем вложенные данные
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')

        # # Создаём или находим пользователя
        user_serializer = UserPassSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Создаем координаты
        coords = CoordPass.objects.create(**coords_data)

        # Создаем сам перевал
        pereval = PerevalAdded.objects.create(user=user, coords=coords, **validated_data)

        # Создаем изображения и связываем их с перевалом
        for image_data in images_data:
            PerevalImages.objects.create(pereval=pereval, **image_data)

        return pereval

class PerevalInfoSerializer(serializers.ModelSerializer):
    user = UserPassSerializer()
    coords = CoordPassSerializer()
    images = PerevalImagesSerializer(many=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'beauty_title', 'title', 'other_titles', 'connect', 'add_time',
            'status', 'user', 'coords',
            'level_winter', 'level_summer', 'level_autumn', 'level_spring',
            'images'
        ]