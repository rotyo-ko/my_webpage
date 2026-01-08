from django.urls import path

from . import views


urlpatterns = [
    path("",views.board, name="board"),
    path("comment_list/", views.comment_list, name="comment_list"),
    path("comment_edit/<int:comment_id>/", views.comment_edit, name="comment_edit"),
    path("comment_delete/<int:comment_id>/", views.comment_delete, name="comment_delete"),
]