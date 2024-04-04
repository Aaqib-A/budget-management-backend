from django.urls import re_path

from category.views.category_view import CategoryView

urlpatterns = [
    re_path(r'^$', CategoryView.as_view()),
]