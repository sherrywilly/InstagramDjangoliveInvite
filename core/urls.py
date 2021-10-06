from django.urls import path

from core.views import LoginView, UserManage, addSlave, dashboard, deleteSlave, logout_view, status_view,tester

urlpatterns = [
path('', LoginView, name="login"),
path('dash/', dashboard, name="dash"),
path('test/<user>/',tester,name="test"),
  path('status/', status_view, name="status"),
    path('logout/', logout_view, name="logout"),
    path('addslave/', addSlave, name="addslave"),
    path('slave/<int:pk>/', deleteSlave, name="sremove"),
    path('user/action/<uuid:pk>', UserManage, name='umanage')
]