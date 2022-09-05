from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .filters import NewsFilter
from .forms import PostForm, UserForm, Post, User, Author
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.shortcuts import redirect
from django.contrib.auth.models import Group


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'news'
    paginate_by = 5
    queryset = Post.objects.filter(type='Новость')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class ArticleList(NewsList):
    queryset = Post.objects.filter(type='Статья')


class NewCreate(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm
    permission_required = 'news.add_post'

    def form_valid(self, form):
        new = form.save(commit=False)
        new.type = "Новость"
        new.author = self.request.user.author
        return super().form_valid(form)


class ArticleCreate(CreateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        new = form.save(commit=False)
        new.type = "Статья"
        new.author = self.request.user.author
        return super().form_valid(form)


class NewDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(type="Новость")


class ArticleDetail(NewDetail):
    """Мне эта маршрутизация не нравится, просто выполняю задание"""
    queryset = Post.objects.filter(type="Статья")


class NewUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    queryset = Post.objects.filter(type="Новость")
    permission_required = ('news.update_post',)

    def get_permission_required(self):
        object = self.get_object()
        if self.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(self.__class__.__name__)
            )
        elif any([object.author.user == self.request.user,
                  self.request.user.is_staff, self.request.user.is_superuser]):
            return self.permission_required
        print('s')
        return ()


class ArticleUpdate(NewUpdate, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    queryset = Post.objects.filter(type="Статья")
    permission_required = ('news.update_post',)


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('main')
    permission_required = ('news.delete_post',)


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


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_edit.html'


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    author = Author(user=user)
    author.save()
    if not user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')


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
