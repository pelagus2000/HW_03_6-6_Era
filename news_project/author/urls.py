from django.urls import path
from .views import ProfileCommonView, upgrade_me

urlpatterns = [
    # Add this
    path('', ProfileCommonView.as_view(), name='users-profile'),
    path('upgrade/', upgrade_me, name='profile_upgrade'),
]