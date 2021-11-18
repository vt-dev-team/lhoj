from django.db import models

# Create your models here.


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.title
    def get_item(self):
        return {
            "id": self.id,
            "title": self.title,
            "pub_date": self.pub_date
        }
    def get_all(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "pub_date": self.pub_date
        }
