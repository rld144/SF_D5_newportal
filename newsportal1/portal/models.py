from django.db import models
from django.contrib.auth.models import User

news = 'news'
article = 'article'
POST_CHOICE = [(news, 'новость'), (article, 'статья')]


# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = 0
        for i in self.post_set.all():
            self.rating += i.rating * 3
        for i in self.user.comment_set.all():
            self.rating += i.rating
        for post in self.post_set.all():
            for i in post.comment_set.all():
                self.rating += i.rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=50)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_choice = models.CharField(choices=POST_CHOICE, default=news, max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.text[:124] + '..'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_rating(self):
        return self.rating


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_rating(self):
        return self.rating