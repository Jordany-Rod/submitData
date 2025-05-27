from django.urls import path
from .views import SubmitData, PerevalReturnId

urlpatterns = [
    path('submitData/', SubmitData.as_view(), name='submit_data'),
    path('submitData/<int:id>/', PerevalReturnId.as_view(), name='submit_data_id'),
]