from django.urls import path
from . import views

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main-page"),
    path("posts", views.AllPostsView.as_view(), name="posts"),
    path("posts/<slug:slug>", views.PostDetailView.as_view(), name="post-detail"),
    path("read-later", views.ReadLaterView.as_view(), name= "read-later"),
]
