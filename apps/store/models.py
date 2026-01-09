from django.db import models
from django.conf import settings
from apps.master.models import BaseModel
import os
# Create your models here.

def blog_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"blogs/temp.{ext}"  # temporary name


class BlogCategory(BaseModel):
    name = models.CharField(max_length=255)


class Blogs(BaseModel):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=blog_image_upload_path,
        default="blogs/default_blog.jpg",
        blank=True,
        null=True
    )
    title = models.CharField(max_length=255)
    content = models.TextField()

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # Get old image
        old_image = None
        if not is_new:
            old_image = Blogs.objects.filter(pk=self.pk).first()

        super().save(*args, **kwargs)

        # ❗ If default image → DO NOTHING
        if not self.image or self.image.name == "blogs/default_blog.jpg":
            return

        # Rename only real uploaded image
        ext = self.image.name.split('.')[-1]
        new_name = f"blogs/blog_{self.id}.{ext}"
        new_path = os.path.join(settings.MEDIA_ROOT, new_name)

        if self.image.path != new_path:
            # Remove old image if exists
            if old_image and old_image.image.name != "blogs/default_blog.jpg":
                if os.path.exists(old_image.image.path):
                    os.remove(old_image.image.path)

            os.rename(self.image.path, new_path)
            self.image.name = new_name
            super().save(update_fields=["image"])