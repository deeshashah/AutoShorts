from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^latestnews/', views.latestnews, name='latestnews'),
]
