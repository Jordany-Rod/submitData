"""
Описание моделей REST API для проекта ФСТР (Федерация спортивного туризма России).
1. Модель пользователя (UserPass) содержит email, имя, фамилию, отчество, номер телефона (не обязательно).
2. Модель координат перевала (CoordPass) содержит широту, долготу и высоту над уровнем моря перевала.
3. Модель изображений перевала (PerevalImages) связана с конкретным перевалом. Содержит название изображения и ссылку.
4. Основная модель перевала (PerevalAdded) включает всю информацию о перевале.
            - Названия
            - Дата добавления
            - Описание соединений
            - Сложность прохождения по сезонам (зима, весна, лето, осень)
            - Статус модерации (импортируется из файла resources: новая, на модерации, принята, отклонена)
Связи между моделями:
1. Перевал связан с пользователем через ForeignKey.
2. Координаты перевала задаются как уникальная запись OneToOneField.
3. Изображения привязаны к перевалу через ForeignKey.

"""

from django.db import models
from django.utils import timezone
from submitData.resources import STATUS_DATA

class UserPass(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    fam = models.CharField(max_length=100)
    otc = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.name} {self.fam} ({self.email})'

class CoordPass(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    def __str__(self):
        return f'Широта: {self.latitude}, Долгота: {self.longitude}, Высота: {self.height}'

class PerevalAdded(models.Model):
    beauty_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=255, blank=True)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField(default=timezone.now)

    level_winter = models.CharField(max_length=3, blank=True)
    level_summer = models.CharField(max_length=3, blank=True)
    level_autumn = models.CharField(max_length=3, blank=True)
    level_spring = models.CharField(max_length=3, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_DATA, default='new')

    # связи
    user = models.ForeignKey(UserPass, on_delete=models.CASCADE, related_name='perevals')
    coords = models.OneToOneField(CoordPass, on_delete=models.CASCADE, related_name='pereval')

    def __str__(self):
        return f'{self.beauty_title} {self.title} ({self.add_time.strftime("%Y-%m-%d")})'

class PerevalImages(models.Model):
    pereval = models.ForeignKey('PerevalAdded', on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=100)
    image_url = models.URLField()

    def __str__(self):
        return f'{self.title} - {self.image_url}'