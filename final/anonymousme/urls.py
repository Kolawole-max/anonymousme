from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('anonymous', views.landingpage, name='landingpage'),
    path("anonymous/login", views.login_view, name="login"),
    path("anonymous/logout", views.logout_view, name="logout"),
    path("anonymous/register", views.register, name="register"),
    path("anonymous/profile/<str:user_username>", views.profile, name="index"),
    path('send/<str:username>', views.send, name='send'),

    # Fetch API
    path('load/<str:username>/', views.load, name='load')
] + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)