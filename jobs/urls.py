from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path("employer/applications/", views.employer_applications, name="employer_applications"),
    path('create/', views.job_create, name='create_job'),
    path('job_details/<int:pk>/', views.job_detail, name='job_detail'),
    
    path('<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path("applications/<int:application_id>/accept/", views.accept_application, name="accept_application"),
    path("applications/<int:application_id>/decline/", views.decline_application, name="decline_application"),
    path("my-applications/", views.my_applications, name="my_applications"),
    
    path('feed/', views.feed, name='feed'),
    path('create_post/', views.create_post, name='create_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),


]
