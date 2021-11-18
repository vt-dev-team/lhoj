from django.db import models
from django.db.models.lookups import EndsWith


class Contest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tp = models.IntegerField(default=0)
    problems = models.CharField(max_length=500, default="")
    privilege = models.IntegerField(default=16)

    def __str__(self):
        return "Contest#{} {}".format(self.id, self.title)

    def get_simple(self):
        return {
            "id": self.id,
            "title": self.title,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "tp": self.tp,
            "problems": self.problems,
            "privilege": self.privilege,
        }
    def get_all(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "tp": self.tp,
            "problems": self.problems,
            "privilege": self.privilege,
        }
