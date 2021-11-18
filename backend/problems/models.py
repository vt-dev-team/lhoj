from django.db import models

# Create your models here.


class Problem(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=262144)
    judge_type = models.IntegerField(default=0)
    tags = models.CharField(max_length=200)
    difficulty = models.IntegerField(default=0)
    algorithms = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return '#' + str(self.id) + ' ' + self.title

    def get_simple(self):
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags,
            "algorithms": self.algorithms,
            "pub_date": self.pub_date
        }

    def get_all(self):
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags,
            "time_limit": self.time_limit,
            "memory_limit": self.memory_limit,
            "judge_type": self.judge_type,
            "content": self.content,
            "difficulty": self.difficulty,
            "algorithms": self.algorithms,
            "author": self.author,
            "pub_date": self.pub_date
        }
