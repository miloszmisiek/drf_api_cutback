from django.contrib import admin
from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from .views import root_route, logout_route

urlpatterns = [
    path('', root_route),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path(
        'dj-rest-auth/registration/',
        include('dj_rest_auth.registration.urls')
    ),
    path(
        'verify-email/',
        VerifyEmailView.as_view(),
        name='rest_verify_email'
    ),
    path(
        'account-confirm-email/',
        VerifyEmailView.as_view(),
        name='account_email_verification_sent'
    ),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        VerifyEmailView.as_view(), name='account_confirm_email'
    ),
    path('password-reset/', PasswordResetView.as_view()),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('', include('profiles.urls')),
    path('', include('products.urls')),
    path('', include('ratings.urls')),
    path('', include('comments.urls')),
]
