from __future__ import unicode_literals


from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.

def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s" %(instance.id, instance.id, extension)
    return "%s/%s" %(instance.id, filename)


#Post.objects.all()
#Post.object.all() = super(PostManager, self).all()
#Post.objects.creatE(user=user, title="Some time")

class PostManager(models.Manager):
    def active (self, *args, **kwargs):
        return super(PostManager, self).filter(
            publish__lte=timezone.now(),
            draft=False)




class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    title = models.CharField(max_length=120)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True, auto_now_add=False)

    image = models.ImageField(upload_to=upload_location,
            null=True,
            blank=True, 
            width_field="width_field",
            height_field="height_field")

    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    slug = models.SlugField(max_length=120, unique=True)

    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
    	# return reverse("posts:detail", kwargs={'id': self.id})
        return reverse("posts:detail", kwargs={'id': self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated_time"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    # slug = slugify(instance.title)
    # #Tesla item 1" -> "tesla-item-1"
    # exists = Post.objects.filter(slug=slug).exists()
    # if exists:
    #     slug = "%s-%s" %(slug, instance.id)
    # instance.slug = slug



pre_save.connect(pre_save_post_receiver, sender=Post)


