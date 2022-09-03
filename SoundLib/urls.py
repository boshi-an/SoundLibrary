"""SoundLib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views

from django.urls import include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [path('i18n/', include('django.conf.urls.i18n')),]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.hello, name="root"),
    path('index/<str:tag>/<int:page>/', views.hello, name="index"),
    path('index/<str:tag>/', views.hello),
    path('upload/', views.upload, name="upload"),
    path('login/', views.login, name="login"),
    path('login/login/', views.login_form, name="login_form"),
    path('login/register/', views.register_form, name="register_form"),
    path('logout/', views.logout, name="logout"),
    path('user/<str:username>/', views.user_info, name="user_info"),
    path('user/<str:username>/change/', views.user_info_change, name="user_info_change"),
    path('user/<str:username>/change/commit/', views.user_info_change_commit, name="user_info_change_commit"),
    path('user/<str:username>/verify/', views.verify_email, name="verify_email"),
    path('user/<str:username>/verify/<str:code>/', views.verify_email_process, name="verify_email_process"),
    path('recording/<int:id>/', views.recording_info, name="recording_info"),
    path('recording/<int:id>/change/', views.recording_change, name="recording_change"),
    path('recording/<int:id>/change/commit/', views.recording_change_commit, name="recording_change_commit"),
    path('composer/<int:id>/', views.composer_info, name="composer_info"),
    path('composer/<int:id>/change/', views.composer_change, name="composer_change"),
    path('composer/<int:id>/change/commit/', views.composer_change_commit, name="composer_change_commit"),
    path('error/verification_needed/', views.error_email_not_verified, name="error_email_not_verified"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
        name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name="password_reset_complete",
    ),
    prefix_default_language = True
)

if settings.DEBUG: # in debug mode, django doesn't support media url
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
