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

def product_image_path(instance, filename):
    """
    Upload images inside:
    products/product_<id>/filename
    Safe even before instance.id exists
    """
    product_id = instance.id or "temp"
    return f"products/product_{product_id}/{filename}"


class ProductCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.CharField(max_length=50)
    content = models.TextField()
    additional_details = models.JSONField(blank=True, null=True)

    image_1 = models.ImageField(
        upload_to=product_image_path,
        default="products/default_product.jpg",
        blank=True,
        null=True
    )
    image_2 = models.ImageField(
        upload_to=product_image_path,
        blank=True,
        null=True
    )
    image_3 = models.ImageField(
        upload_to=product_image_path,
        blank=True,
        null=True
    )
    image_4 = models.ImageField(
        upload_to=product_image_path,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    # ⭐ PRIMARY IMAGE LOGIC
    def primary_image(self):
        if self.image_1:
            return self.image_1.url
        return settings.MEDIA_URL + "products/default_product.jpg"