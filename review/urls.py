from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'review', views.ReviewListCreateView.as_view(), name='reviews')
]
