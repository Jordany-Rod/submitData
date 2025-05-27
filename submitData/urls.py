from django.urls import path
from .views import SubmitData, PerevalReturnIdUpdate

urlpatterns = [
    path('submitData/', SubmitData.as_view(), name='submit_data'),
    path('submitData/<int:id>/', PerevalReturnIdUpdate.as_view(), name='submit_data_id'),
]