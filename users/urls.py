from django.urls import path
from .views import InviteUserView

urlpatterns = [
    path('admin/invite/', InviteUserView.as_view(), name='invite-user'),
]