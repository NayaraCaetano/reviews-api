from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    url(r'sign-in', views.UserSignInView.as_view(), name='user_sign_in'),
    url(r'login', obtain_jwt_token, name='user_login')
]
