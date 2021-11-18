from django.db import models

"""
0   Pending
1   Pending Rejudge
2   Judging
3   Accepted
4   Wrong Answer
5   Time Limit Exceeded
6   Memory Limit Exceeded
7   Output Limit Exceeded
8   Runtime Error
9   Unknown Error
10  System Error
11  Unaccepted
"""


class Submission(models.Model):
    user_id = models.CharField(max_length=50)
    code = models.TextField()
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    result = models.IntegerField(default=0)
    problem = models.IntegerField(default=1)
    contest = models.IntegerField(default=0)
    cases = models.TextField()
    judger = models.CharField(max_length=50)
    date = models.DateTimeField('date')

    def __str__(self):
        return "Submission#{} {}".format(self.id, self.result)

    def get_simple(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "time": self.time,
            "memory": self.memory,
            "score": self.score,
            "judger": self.judger,
            "problem": self.problem,
            "contest": self.contest,
            "result": self.result,
            "date": str(self.date)
        }

    def get_all(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "code": self.code,
            "time": self.time,
            "memory": self.memory,
            "score": self.score,
            "result": self.result,
            "cases": self.cases,
            "judger": self.judger,
            "problem": self.problem,
            "contest": self.contest,
            "date": str(self.date),
        }
