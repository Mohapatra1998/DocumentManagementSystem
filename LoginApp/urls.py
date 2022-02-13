from django.urls import path
from LoginApp import views
urlpatterns = [
    path('', views.user_login, name='login'),
    path('document/drawnig/no/<str:id>',  views.qr_scanner_page, name='qr_scanner_page'),
    path('scanner_login',  views.scanner_login, name='scanner_login'),
]
