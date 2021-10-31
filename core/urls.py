from django.urls import path

from core.views import ImageUpload, LoginView, UserManage, addSlave, dashboard, deleteSlave, insta_invite, logout_view, status_view, tester, fetch_users, userImage

urlpatterns = [
    path('', LoginView, name="login"),
    path('dash/', dashboard, name="dash"),
    path('test/<user>/', tester, name="test"),
    path('status/', status_view, name="status"),
    path('logout/', logout_view, name="logout"),
    path('addslave/', addSlave, name="addslave"),
    path('slave/<int:pk>/', deleteSlave, name="sremove"),
    path('user/action/<uuid:pk>', UserManage, name='umanage'),
    path('fetch_users/', fetch_users, name="test"),
    path('invite/', insta_invite, name="invitor"),
    path('get_img',userImage,name="getimg"),
    path('image_upload',ImageUpload,name="imageupload")
]
