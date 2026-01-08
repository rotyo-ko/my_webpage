from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import CommentForm
from .models import Comment


# comments = []　最初はcommentsリストに保存
def board(request):
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # まだDBに保存しない
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()                    # ここで保存
            # name = form.cleaned_data["name"]         
            # message = form.cleaned_data["message"]
            # date = datetime.now.strftime("%Y-%m-%d")
            # comments.insert(0, {"name": name,
            #                     "message: message",
            #                     "date": date})
            return redirect("board") # これは必要か？→２重投稿防止になる。
                                     # redirectしないと投稿フォームに入力が残るのでredirectしたほうがいい

    else:
        form = CommentForm()
        
    comments = Comment.objects.all()
    paginator = Paginator(comments, 5)
    page = request.GET.get("page", 1)
    try:
        comments = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        comments = paginator.page(1)

    return render(request, "board.html",
                  {"form": form,
                   "comments": comments})


@login_required
def comment_list(request):
    comments = Comment.objects.filter(user=request.user)
    paginator = Paginator(comments, 5)
    page = request.GET.get("page", 1)
    try:
        comments = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        comments = paginator.page(1)
    
    return render(request, "comment_list.html",
                   {"comments": comments})

@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            if not comment.message.strip().startswith("(修正済み)"):
                comment.message = "(修正済み)" + comment.message
            comment.save()
            return redirect("comment_list")
    else:
        form = CommentForm(instance=comment)
    return render(request, "comment_edit.html",
                 {"form": form})

@login_required
def comment_delete(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id, user=request.user) # user=request.userでログインユーザ―以外できないようにする
        comment.delete()
        return redirect("comment_list")
    else:
        return render(request, "comment_delete.html")

