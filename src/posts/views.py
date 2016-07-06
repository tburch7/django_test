from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Post

# Create your views here.
def post_list(request):
	queryset = Post.objects.all()

	context = {
		"object_list": queryset,
		"title": "List"
	}
	return render(request, "index.html", context)
	#HttpResponse("<h1> Post List! </h1>")


def post_create(request):
	return HttpResponse("<h1> Post Create! </h1>")


def post_detail(request, id=None): #retrieve
	
	#instance = Post.objects.get(id=1)
	instance = get_object_or_404(Post, id=id)
	context = {
		"title": instance.title,
		"instance": instance,

	}
	return render(request, "post_detail.html", context) 
	#HttpResponse("<h1> Post Detail! </h1>")


def post_update(request):
	return HttpResponse("<h1> Post Update! </h1>")


def post_delete(request):
	return HttpResponse("<h1> Hello Post Delete! </h1>")