from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ["id", "message", "date", "name", "user"]
        read_only_fields = ["user"] # "user"を入力不可に
    
    def get_name(self, obj):
        return obj.name()
