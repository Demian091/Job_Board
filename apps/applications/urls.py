from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('my-applications/', views.MyApplicationsView.as_view(), name='my_applications'),
    path('<int:pk>/', views.ApplicationDetailView.as_view(), name='detail'),
    path('manage/', views.ManageApplicationsView.as_view(), name='manage'),
    path('<int:pk>/update-status/', views.UpdateApplicationStatusView.as_view(), name='update_status'),
]