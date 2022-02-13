from django.urls import path, include
from ManagerApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('managerdashboard/', views.manager_dashboard, name='managerdashboard'),
    path('managerlogout/', views.managerlogout, name='managerlogout'),
    path('managerviewdocument/', views.view_document, name='managerviewdocument'),
    path('manager_document_details/<str:id>', views.document_details, name='manager_document_details'),
    path('searchmanager/', views.search_manager, name='searchmanager'),
    path('approvestatus1/', views.approve_status, name='approvestatus1'),
    path('ad_search_form/', views.ad_search_form, name='ad_search_form'),
    path('ad_search_manager/', views.ad_search_manager, name='ad_search_manager'),

    #path('manager_reject_form/', views.manager_reject_form, name='manager_reject_form'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
