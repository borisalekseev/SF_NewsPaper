from django.urls import path
from .views import NewsSearch, posts_dispatcher, post_create_dispatcher, post_detail_dispatcher, post_update_dispatcher


urlpatterns = [
    path('', posts_dispatcher),
    path('search/', NewsSearch.as_view(), name='post_search'),
    path('create/', post_create_dispatcher, name='post_create'),
    path('<int:pk>/', post_detail_dispatcher, name='post_detail'),
    path('<int:pk>/update/', post_update_dispatcher, name='post_update'),
    path('<int:pk>/delete/', post_detail_dispatcher, name='post_delete')
]
