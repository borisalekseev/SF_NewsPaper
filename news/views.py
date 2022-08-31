from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post
from .filters import NewsFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'news'
    paginate_by = 5
    queryset = Post.objects.filter(type='Новость')


class ArticleList(NewsList):
    queryset = Post.objects.filter(type='Статья')


class NewCreate(CreateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        product = form.save(commit=False)
        product.type = "Новость"
        return super().form_valid(form)


class ArticleCreate(CreateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        product = form.save(commit=False)
        product.type = "Статья"
        return super().form_valid(form)


class NewDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(type="Новость")


class ArticleDetail(NewDetail):
    """Мне эта маршрутизация не нравится, просто выполняю задание"""
    queryset = Post.objects.filter(type="Статья")


class NewUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    queryset = Post.objects.filter(type="Новость")


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    queryset = Post.objects.filter(type="Статья")


class NewsSearch(NewsList):
    template_name = 'posts_search.html'
    queryset = Post.objects.filter(type='Новость')
    filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


VIEW_CHOICES = {
    'posts': {'news': NewsList.as_view(), 'articles': ArticleList.as_view()},
    'create': {'news': NewCreate.as_view(), 'articles': ArticleCreate.as_view()},
    'detail': {'news': NewDetail.as_view(), 'articles': ArticleDetail.as_view()},
    'update': {'news': NewUpdate.as_view(), 'articles': ArticleUpdate.as_view()}
}


def posts_dispatcher(request): return VIEW_CHOICES['posts'][request.path.split('/')[1]](request)
def post_create_dispatcher(request): return VIEW_CHOICES['create'][request.path.split('/')[1]](request)


def post_detail_dispatcher(request, **kwargs):
    return VIEW_CHOICES['detail'][request.path.split('/')[1]](request, **kwargs)


def post_update_dispatcher(request, **kwargs):
    return VIEW_CHOICES['update'][request.path.split('/')[1]](request, **kwargs)


def post_delete_dispatcher(request, **kwargs):
    return VIEW_CHOICES['delete'][request.path.split('/')[1]](request, **kwargs)