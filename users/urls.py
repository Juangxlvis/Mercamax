from django.urls import path
from .views import InviteUserView,ActivateAccountView

urlpatterns = [
    path('admin/invite/', InviteUserView.as_view(), name='invite-user'),
    path('activate-account/', ActivateAccountView.as_view(), name='activate-account'),
]