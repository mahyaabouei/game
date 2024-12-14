from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.MissionsViewSet, basename='missions')

urlpatterns = [
    path('missions/<int:mission>/', views.MissionsViewSet.as_view() , name='missions'),
    path('missions/', views.MissionsViewSet.as_view() , name='missions'),
    path('show-user-mission/', views.ShowUserMission.as_view() , name='show-user-mission'),
    path('gift/', views.GiftView.as_view() , name='gift'),
]

