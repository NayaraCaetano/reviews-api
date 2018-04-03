from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'sign-in', views.UserSignInView.as_view(), name='user_sign_in'),
]
