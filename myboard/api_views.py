from rest_framework import viewsets, filters
from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # 読み取りは誰でもok オブジェクトの権限なのでpostには影響しない
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        # 編集・削除は本人のみ
        return obj.user == request.user

class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    # だれでも編集削除できる状況を避けるためにGETだけを行うようにする
    # MyCommentViewSetに未ログイン時の投稿の処理をさせる。
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date"]
    ordering = ["-date"] # modelで"-date"でorderingされているがViewSetが優先される。どちらも"-date"なので変わらない。
    
class MyCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        # 未ログイン時は空のオブジェクトを返す
        if not self.request.user.is_authenticated:
            return Comment.objects.none()
        return Comment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None
        # これでCommentモデルの
        # def name(self)のself.user ならself.user.usernameをかえし、
        # それいがい(None)なら"ゲスト"を返すようにできる。
        serializer.save(user=user)



    

    