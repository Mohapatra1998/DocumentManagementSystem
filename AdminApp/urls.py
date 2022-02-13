from django.urls import path
from AdminApp import views
urlpatterns = [
    path('admindashboard/', views.admin_dashboard, name='admindashboard'),
    path('viewuser/', views.view_user, name='viewuser'),
    path('viewmanager/', views.view_manager, name='viewmanager'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('addmanager/', views.add_manager, name='addmanager'),
    path('adduser/', views.add_user, name='adduser'),
    path('adminviewdocument/', views.view_document, name='adminviewdocument'),
    path('admin_document_details/<str:id>', views.document_details, name='admin_document_details'),
    path('searchadmin/', views.search_admin, name='searchadmin'),
    path('approvestatusadmin/', views.approve_status, name='approvestatusadmin'),
     path('ad_search_form1/', views.ad_search_form1, name='ad_search_form1'),
    path('ad_search_admin/', views.ad_search_admin, name='ad_search_admin'),

]
