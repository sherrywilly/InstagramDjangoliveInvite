from django.urls import path

from core.views import LoginView, dashboard,tester

urlpatterns = [
path('', LoginView, name="login"),
path('dash/', dashboard, name="dash"),
path('test/<user>/',tester,name="test")
]