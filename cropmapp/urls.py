from django.urls import path
from .views import *
urlpatterns = [
    path('predict/', PredictDisease.as_view(), name='predict_disease'),
    path('superuser-login/', SuperuserLoginView.as_view(), name='superuser-login'),
    path('forgot-password/',ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('schemesadd/',SchemeListCreateView.as_view(),name="schmea"),
    path('schemeupdate/<pk>',SchemeUpdateDelete.as_view(),name='schemeupdate'),
    path('crop-recommendation/', CropRecommendationAPIView.as_view(), name='crop-recommendation'),
    path('equipmentadd/',EquipmentListCreateView.as_view(),name="schmea"),
     path('equipmentupdate/<pk>',EquipmentUpdateDelete.as_view()),
    path('register/',RegistrationView.as_view(),name="reg"),
    path('login/',UnifiedLoginView.as_view()),
    path('allschemeview/',UserSchemeListView.as_view()),
    path('schemes/<int:pk>/', UserSchemeDetailView.as_view(), name='user-scheme-detail'),
    path('usermanage/',UserListView.as_view()),
    path('add-to-cart/', AddToCartAPIView.as_view(), name='add-to-cart'),
     path('equipment/', EquipmentAddApiView.as_view(), name='equipment-list'),
    path('equipment/<int:pk>/', EquipmentAddApiView.as_view(), name='equipment-detail'),
    path('create-order/', OrderCreateAPIView.as_view(), name='create-order'),
    path('farmerproducts/', FarmerProductAPIView.as_view(), name='farmer-product-list'),
    
    

    

]