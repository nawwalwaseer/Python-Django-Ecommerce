from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey 


class TagItemManager(models.Manager):
    def get_tags_for(self, object_type, obj_id):
        content_type = ContentType.objects.get_for_model(object_type)
        return TagItem.objects.select_related('tag').filter(
             content_type=content_type,
             object_id= obj_id
        )

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

class TagItem(models.Model):
    objects = TagItemManager()

    # a tag will be linekd to every tag item
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # what tag each item belongs to for this we need two things
    # Type & Id

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey() # to define generic relationship we need three things content_type, object_id and content_object