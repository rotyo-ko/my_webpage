from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from myboard.models import Comment
from myboard.forms import CustomAuthenticationForm


class TestBoard(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="テスト1",password="test1")
        self.comment = Comment.objects.create(user=self.user, message="テストメッセージ")
    
    def test_board_get(self):
        res = self.client.get(reverse("board"))
        self.assertTemplateUsed(res, "board.html")
        self.assertContains(res, "テストメッセージ") 
        self.assertIn("comments", res.context)

    def test_board_post_without_login(self):
        """
        ログインしていないユーザーが投稿したときの挙動をチェック
        """
        res1 = self.client.post(
            reverse("board"),
            data={"message": "ポストメッセージ"},
            ) # follow=True を書くとリダイレクト先の最終ページまでのレスポンスres1に入る
        res2 = self.client.get(reverse("board"))
        self.assertEqual(res1.status_code, 302)
        self.assertTemplateUsed(res2, "board.html")
        self.assertTrue(Comment.objects.filter(message="ポストメッセージ").exists())
        # postされたメッセージをさがしてユーザー名がないか確認
        new_comment = Comment.objects.get(message="ポストメッセージ")
        self.assertIsNone(new_comment.user)
        self.assertRedirects(res1, reverse("board"))
        self.assertContains(res2, "ポストメッセージ")
        self.assertContains(res2, "ゲスト")

    def test_board_post_with_login(self):
        
        form = CustomAuthenticationForm(data={"username": "テスト1", "password":"test2"})
        # ログイン
        self.client.post(reverse("login"),
                    data={"username": "テスト1", "password":"test1"})
        # 投稿
        res1 = self.client.post(
            reverse("board"),
            data={"message":"ポストメッセージ2"}
            )
        # get
        res2 = self.client.get(reverse("board"))
        self.assertEqual(res2.status_code, 200)
        
        new_comment = Comment.objects.get(message="ポストメッセージ2")
        self.assertEqual(new_comment.user, self.user)
        # new_comment.user.username == "テスト1"ではなくオブジェクトのチェックのほうが堅牢
        self.assertRedirects(res1, reverse("board"))
        self.assertContains(res2, "ポストメッセージ2")
        self.assertContains(res2, "テスト1")

class TestCommentList(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test1",password="test1")
        self.client.force_login(self.user)
        self.comment = Comment.objects.create(user=self.user, message="message1")
        #　これでself.userのコメントになる
    
    def test_comment_list_get(self):
        res = self.client.get(reverse("comment_list"))
        self.assertTemplateUsed(res, "comment_list.html")
        self.assertContains(res, "message1") 
        self.assertIn("comments", res.context)

    def test_comment_edit_get(self):
        res = self.client.get(reverse("comment_edit", args=(self.comment.id,)))
        
        self.assertTemplateUsed(res, "comment_edit.html")
        self.assertEqual(res.context["form"].instance, self.comment)
    
    def test_comment_edit_post(self):
        res = self.client.post(reverse("comment_edit", args=(self.comment.id,)),
                               data={"message":"edit_message"})
        self.assertRedirects(res, reverse("comment_list"))
        self.assertTrue(Comment.objects.filter(message="(修正済み)edit_message",
                                               user=self.user).exists())
        
    def test_comment_delete(self):
        res = self.client.post(reverse("comment_delete", args=(self.comment.id,)))
        self.assertRedirects(res, reverse("comment_list"))
        self.assertFalse(Comment.objects.filter(message="message1",
                                                user=self.user).exists())
        self.assertEqual(Comment.objects.count(), 0)
        

class TestLoginRequiered(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.comment = Comment.objects.create(user=self.user, message="test1")
    def test_comment_list_without_login(self):
        res = self.client.get(reverse("comment_edit", args=(self.comment.id,)))
        self.assertEqual(res.status_code, 302)
        self.assertIn("/accounts/login/", res.url)
        self.assertIn("?next=", res.url)

    def test_comment_delete_without_login(self):
        res = self.client.get(reverse("comment_delete", args=(self.comment.id,)))
        self.assertEqual(res.status_code, 302)
        self.assertIn("/accounts/login/", res.url)
        self.assertIn("?next=", res.url)

class TestOtherComment(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username="test", password="test")
        self.client.force_login(self.user)
        
    def test_comment_edit_other(self):
        user1 = User.objects.create_user(username="test1", password="test1")
        comment = Comment.objects.create(user=user1, message="test")
        res = self.client.post(reverse("comment_edit", args=(comment.id,)),
                               data={"message":"edit_message"})
        self.assertEqual(res.status_code, 404)

    def test_comment_delete_other(self):
        user1 = User.objects.create_user(username="test1", password="test1")
        comment = Comment.objects.create(user=user1, message="test")
        res = self.client.post(reverse("comment_delete", args=(comment.id,)))
        self.assertEqual(res.status_code, 404)

