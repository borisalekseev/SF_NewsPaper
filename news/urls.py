from django.urls import path
from .views import NewsSearch, posts_dispatcher, post_create_dispatcher, post_detail_dispatcher,\
    post_update_dispatcher, PostDelete, become_author
from django.views.generic import TemplateView

urlpatterns = [
    path('', posts_dispatcher, name='main'),
    path('search/', NewsSearch.as_view(), name='post_search'),
    path('create/', post_create_dispatcher, name='post_create'),
    path('<int:pk>/', post_detail_dispatcher, name='post_detail'),
    path('<int:pk>/update/', post_update_dispatcher, name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('permission_denied/', TemplateView.as_view(template_name='permission_denied.html'), name='permission_denied'),
    path('author/', become_author, name='become_author')
]
