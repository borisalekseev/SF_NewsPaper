from django_filters import FilterSet, filters, widgets
from .models import Post, Category


class NewsFilter(FilterSet):
    category = filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), label='Категория')
    date = filters.DateFromToRangeFilter(widget=widgets.DateRangeWidget(attrs={'type': 'date'}), label='Дата')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок')

    class Meta:
        model = Post
        fields = []
