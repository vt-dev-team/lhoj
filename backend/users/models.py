from django.db import models

"""
# Privilege
1	    访问主站
2	    提交题目
4	    查看题目
8	    查看他人代码
16	    参加比赛
32	    使用博客
64	    发送私信
128	    自由发言
256	    添加题目
512	    举办比赛
1024	获取题目数据
2048	编辑题目
4096	管理比赛
8192	管理发言
16384	管理权限
32768   操作提交记录
65536   下载题目数据
"""


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    motto = models.CharField(max_length=200)
    privilege = models.IntegerField(default=247)
    rating = models.IntegerField(default=2500)
    reg_time = models.DateTimeField('date reg')

    def __str__(self):
        return "#{} {}".format(self.id, self.username)

    def get_all(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "motto": self.motto,
            "privilege": self.privilege,
            "rating": self.rating,
            "reg_time": self.reg_time
        }

    def get_simple(self):
        return {
            "id": self.id,
            "username": self.username,
            "motto": self.motto,
            "rating": self.rating
        }


class Message(models.Model):
    from_user = models.CharField(max_length=50)
    to_user = models.CharField(max_length=50)
    content = models.TextField()
    isRead = models.BooleanField(default=False)
    date = models.DateTimeField('date reg')

    def get_all(self):
        return {
            "from_user": self.from_user,
            "to_user": self.to_user,
            "content": self.content,
            "isRead": self.isRead,
            "date": self.date,
        }
