from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from myboard import api_views as comment_api_views


router = routers.DefaultRouter()
router.register("comments", comment_api_views.CommentViewSet)
router.register("my-comments", comment_api_views.MyCommentViewSet, basename="my-comments") # basenameが必要

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("myboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
