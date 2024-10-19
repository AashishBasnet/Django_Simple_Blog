from datetime import date
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Post

from .forms import CommentForm

# Create your views here.


class MainPageView(ListView):
    template_name = "blog/main_page.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        query_set = super().get_queryset()
        data = query_set[:3]
        return data


class AllPostsView(ListView):
    template_name = "blog/posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class PostDetailView(View):
    def is_stored_post(self,request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later


    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
       
        context = {
          "post": post,
          "tags": post.tags.all(),
          "comment_form": CommentForm(),
          "comments":post.comments.all(),
          "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blog/post_detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
          comment = comment_form.save(commit=False)
          comment.post = post
          comment.save()
          
          return HttpResponseRedirect(reverse("post-detail", args=[slug]))

        context = {
          "post": post,
          "tags": post.tags.all(),
          "comment_form": comment_form,
          "comments":post.comments.all().order_by("-id"),
          "saved_for_later": self.is_stored_post(request, post.id),

        }
        return render(request, "blog/post_detail.html", context)

class ReadLaterView(View):

    def get(self,request):
        stored_post = request.session.get("stored_posts")

        context = {}

        if stored_post is None or len(stored_post) ==0:
            context["posts"] = []
            context["has_posts"] = False
        
        else:
            posts = Post.objects.filter(id__in = stored_post)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)
    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
            
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")



# If you only want details:
# class postDetailView(DetailView):
#     template_name = "blog/post_detail.html"
#     model = Post
#     def get_context_data(self, **kwargs) :
#         context = super().get_context_data(**kwargs)
#         context["tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm()
#         return context


# -----------------FUNCTION IMPLEMENTATION OF CLASSES

# def main_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/main_page.html", {
#         "latest_posts": latest_posts
#     })


# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request, "blog/posts.html", {
#         "all_posts": all_posts
#     })


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post_detail.html",
#                   {
#                       "post": identified_post,
#                       "tags": identified_post.tags.all()
#                   })
