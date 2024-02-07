from django.urls import path
from .views import *
urlpatterns = [
    path('solution/', PlantDiseaseDetectionAPIView.as_view(), name='solution-api'),
    path('superuser-login/', SuperuserLoginView.as_view(), name='superuser-login'),
    path('adminforgot/',ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('schemesadd/',SchemeListCreateView.as_view(),name="schmea"),
    path('schemeupdate/<pk>',SchemeUpdateDelete.as_view(),name='schemeupdate'),
    path('crop-recommendation/', CropRecommendationAPIView.as_view(), name='crop-recommendation'),
    path('equipmentadd/',EquipmentListCreateView.as_view(),name="schmea"),
     path('equipmentupdate/<pk>',EquipmentUpdateDelete.as_view()),
    path('register/',FarmerRegistrationView.as_view(),name="reg"),
     path('famerlogin/', FarmerLoginView.as_view(), name='custom_login'),
]