from django.contrib import admin

# Register your models here.
from posts.models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated_time", "timestamp"]
	list_display_links = ["updated_time"]
	list_filter = ["updated_time", "timestamp"]
	list_editable=["title"]
	search_fields = ["title", "content"]
	
	class Meta:
		model = Post

admin.site.register(Post, PostModelAdmin)