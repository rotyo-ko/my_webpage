from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="投稿者")
    message = models.CharField(verbose_name="メッセージ", max_length=120)
    date = models.DateTimeField(verbose_name="投稿日時", auto_now_add=True)

    class Meta:
        db_table = "comment"
        ordering = ("-date",)

    def name(self):
        if self.user:
            return self.user.username  # Userの属性usernameを返す
        else:
            return "ゲスト"




