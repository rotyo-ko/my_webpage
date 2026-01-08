from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Comment


class CommentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")
        self.comment = Comment.objects.create(message="test_message", user=self.user)
    
    def test_get_comments(self):
        res = self.client.get("/api/comments/")
        self.assertEqual(res.status_code, 200)
        # ページネーションが有効になっているのでクエリセットはres.data["results"]に格納されている
        self.assertEqual(len(res.data["results"]), 1) 
        self.assertEqual(res.data["results"][0]["name"], "test")
        self.assertEqual(res.data["results"][0]["message"], "test_message")
        
    def test_get_comments_id(self):
        res = self.client.get(f"/api/comments/{self.comment.pk}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["message"], "test_message")
        self.assertEqual(res.data["name"], "test")
    
    def test_not_allowed_without_get(self):
        # get以外のリクエストが許可されていないことを確認
        url = "/api/comments/"
        url_detail = f"/api/comments/{self.comment.pk}/"

        self.assertEqual(self.client.post(url, data={}).status_code, 405)
        self.assertEqual(self.client.put(url, data={}).status_code, 405)
        self.assertEqual(self.client.patch(url, data={}).status_code, 405)
        self.assertEqual(self.client.delete(url).status_code, 405)
        
        self.assertEqual(self.client.post(url_detail, data={}).status_code, 405)
        self.assertEqual(self.client.put(url_detail, data={}).status_code, 405)
        self.assertEqual(self.client.patch(url_detail, data={}).status_code, 405)
        self.assertEqual(self.client.delete(url_detail).status_code, 405)
    

class MyCommentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")
        self.comment = Comment.objects.create(message="test_message", user=self.user)
        self.client.login(username="test", password="pass")
    
    def test_get_comments(self):
        res = self.client.get("/api/my-comments/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]["message"], "test_message")
        # detailもチェック
        res1 = self.client.get(f"/api/my-comments/{self.comment.pk}/")
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res1.data["message"], "test_message")
        self.assertEqual(res1.data["name"], "test")

    def test_get_comment_without_login(self):
        self.client.logout()
        res = self.client.get("/api/my-comments/")
        # getはリクエストはできる
        self.assertEqual(res.status_code, 200)
        # ログインしていないので取得するクエリセットの個数は0になる
        self.assertEqual(len(res.data["results"]), 0)

    def test_post_comments(self):
        res = self.client.post("/api/my-comments/",
                               data={"message":"test_message2"}, follow=True)
        self.assertEqual(res.status_code, 201)
        # res1 = self.client.get("/api/my-comments/")
        print(res.data)
        # self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data["message"], "test_message2")
        self.assertEqual(res.data["name"], "test")
    
    def test_post_comments_without_login(self):
        self.client.logout()
        res = self.client.post("/api/my-comments/", data={"message": "post"})
        self.assertEqual(res.status_code, 201)
        # クエリセットを取得しないので、Permission のIsOwnerOrReadOnlyも影響しない
        print(res.data)
        self.assertEqual(res.data["message"], "post")
        self.assertEqual(res.data["name"], "ゲスト")
    
    def test_delete_comments(self):
        res = self.client.delete(f"/api/my-comments/{self.comment.pk}/")
        # deleteメソッド成功時は statu_codeは204になる
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Comment.objects.count(), 0)

    def test_patch_comments(self):
        res = self.client.patch(f"/api/my-comments/{self.comment.pk}/",
                                data={"message":"edit"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["message"], "edit")
        self.assertEqual(res.data["name"], "test")

    def test_not_allowed_without_login(self):
        # logoutして、get以外のリクエストが許可されていないことを確認
        self.client.logout()

        url = "/api/my-comments/"
        url_detail = f"/api/my-comments/{self.comment.pk}/"
        
        res = self.client.put(url_detail, data={"message": "put"})    
        self.assertEqual(res.status_code, 404)
        # ログアウトしているためクエリセットが取得できないので404が返る
        # Permission のIsOwnerOrReadOnly はよばれない。呼ばれた場合403or401
        # self.assertIn(res.status_code, [401, 403])とかくといい
        res = self.client.patch(url_detail, data={"message": "patch"})
        self.assertEqual(res.status_code, 404)
        
        res = self.client.delete(url_detail)
        self.assertEqual(res.status_code, 404)
                         


