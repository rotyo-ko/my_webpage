from django.urls import path
from .views import BoardView, CommentListView, CommentEditView, CommentDeleteView

urlpatterns = [
    path("",BoardView.as_view(), name="board"),
    path("comment_list/", CommentListView.as_view(),
          name="comment_list"),
    path("comment_edit/<int:pk>/", CommentEditView.as_view(),
          name="comment_edit"),
    path("comment_delete/<int:pk>/", CommentDeleteView.as_view(), name="comment_delete"),
]
