from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, LikeViewSet
from . import views

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)
router.register('likes', LikeViewSet)

urlpatterns = [
    path("jobs/list/", views.jobs_list),
    path("jobs/<int:job_id>/", views.job_detail),
    path("jobs/<int:job_id>/apply/", views.apply_job),

    path("applications/me/", views.my_applications),
    path("applications/employer/", views.employer_applications),
]


urlpatterns += router.urls
