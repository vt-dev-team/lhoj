from django.db import models

# Create your models here.


class Section(models.Model):
    privilege = models.IntegerField(default=128)
    title = models.CharField(max_length=200)

    def __str__(self):
        return "Section#{} {}".format(self.id, self.title)

    def get_all(self):
        return {
            "id": self.id,
            "title": self.title,
            "privilege": self.privilege
        }


class Post(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    content = models.TextField()
    section = models.IntegerField()
    toplevel = models.IntegerField(default=1)
    date = models.DateTimeField('date')

    def __str__(self):
        return "Post#{} {} by {}".format(self.id, self.title, self.author)

    def get_simple(self):
        return {
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "toplevel": self.toplevel,
            "section": self.section,
            "date": self.date
        }

    def get_all(self):
        return {
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "content": self.content,
            "toplevel": self.toplevel,
            "section": self.section,
            "date": self.date
        }


class Comment(models.Model):
    author = models.CharField(max_length=50)
    content = models.TextField()
    post = models.IntegerField()
    date = models.DateTimeField('date')

    def get_all(self):
        return {
            "id": self.id,
            "author": self.author,
            "content": self.content,
            "post": self.post,
            "date": self.date
        }
