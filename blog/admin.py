from django.contrib import admin
from .models import PostModel, AuthorModel, CommentModel


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','post')

# Register your models here.
admin.site.register(PostModel)
admin.site.register(AuthorModel)
admin.site.register(CommentModel,CommentAdmin)


