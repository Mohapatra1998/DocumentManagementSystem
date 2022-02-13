from django.urls import path
from UserApp import views
urlpatterns = [
    path('userdashboard/', views.user_dashboard, name='userdashboard'),
    path('uploaddocument/', views.document_upload, name='uploaddocument'),
    path('viewdocument/', views.view_document, name='viewdocument'),
    path('document_details/<str:id>', views.document_details, name='document_details'),
    path('updatedocument/<str:id>/', views.update_document, name='updatedocument'),
    path('usersearch/', views.search_user, name='usersearch'),
    path('userlogout/',  views.user_logout, name='userlogout'),
    path('ad_search_form2/', views.ad_search_form2, name='ad_search_form2'),
    path('ad_search_user/', views.ad_search_user, name='ad_search_user'),

]
