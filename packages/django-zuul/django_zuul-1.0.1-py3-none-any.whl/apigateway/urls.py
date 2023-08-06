from django.conf.urls import url
from . import views

app_name = 'apigateway'

urlpatterns = [
    url(r'.*', views.gateway.as_view())
]