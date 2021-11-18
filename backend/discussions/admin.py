from django.contrib import admin

# Register your models here.

from .models import Section, Post, Comment
admin.site.register(Section)
admin.site.register(Post)
admin.site.register(Comment)
