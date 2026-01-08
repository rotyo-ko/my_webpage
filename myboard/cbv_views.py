from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages

from .models import Comment
from .forms import CommentForm


class BoardView(ListView, FormMixin):
    model = Comment
    template_name = "board.html"
    paginate_by = 5
    form_class = CommentForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["comments"] = Comment.objects.all()
        context["comments"] = context["object_list"]
        context["form"] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            return redirect(self.get_success_url())
        return self.get(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("board")
    

class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = "comment_list.html"
    paginate_by = 5
    context_object_name = "comments"
    
    def get_queryset(self): 
        return Comment.objects.filter(user=self.request.user)


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = "comment_edit.html"
    form_class = CommentForm
    
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy("comment_list")
    
    def form_valid(self, form):
        comment = form.save(commit=False)
        if not comment.message.strip().startswith("(修正済み)"):
            comment.message = "(修正済み)" + comment.message
        comment.save()
        messages.success(self.request, "コメントを修正しました。")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "コメントを修正できませんでした。")
        return super().form_invalid(form)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "comment_delete.html"
    success_url = reverse_lazy("comment_list")
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "コメントを削除しました。")
        return super().delete(request, *args, **kwargs)