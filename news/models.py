from django.contrib.auth.models import User
from django.db import models

TYPE_CHOICES = (('article', "статья"), ('new', "новость"))


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = sum([i.rating * 3 for i in Post.objects.filter(author=self)]) \
                      + sum([i.rating for i in Comment.objects.filter(post__author=self)]) \
                      + sum([i.rating for i in Comment.objects.filter(post__author=self)])
        self.save()


class Category(models.Model):
    name = models.CharField(unique=True, max_length=45)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=45, choices=TYPE_CHOICES, default='статья')
    date = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return Post.preview(self)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
