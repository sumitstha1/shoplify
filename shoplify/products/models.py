from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Create your models here.
class Category(BaseModel):
    category = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category_image = models.ImageField(upload_to='category')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category

class Brands(BaseModel):
    brand = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    brand_image = models.ImageField(upload_to='brand')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.brand)
        super(Brands, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.brand


class Collection(BaseModel):
    collection = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    collection_image = models.ImageField(upload_to='collection')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.collection)
        super(Collection, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return self.collection

class ColorVariant(BaseModel):
    color = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color

class SizeVariant(BaseModel):
    size = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.size

class Dresses(BaseModel):
    dress_for = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    dress_image = models.ImageField(upload_to='dresses')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.dress_for)
        super(Dresses, self).save(*args, **kwargs)

    def __str__(self):
        return self.dress_for

    def get_dress_count(self):
        return Product.objects.filter(dress = self.dress_for).count()
    
class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    actual_price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    discounted_percentage = models.IntegerField(null=True, blank=True)
    selling_price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_cat')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, related_name='product_brand')
    description = models.TextField()
    size_variant = models.ManyToManyField(SizeVariant, blank=True)
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    is_trending = models.BooleanField(default=False)
    is_offer = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    is_just_arrived = models.BooleanField(default=False)
    dress = models.ForeignKey(Dresses, on_delete=models.CASCADE, related_name='product_dress', null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='product_collection', null=True, blank=True)
    stock = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if self.discounted_percentage:
            self.discount_price = self.discounted_percentage / 100 * self.actual_price
            self.selling_price = self.actual_price - self.discount_price
            self.is_offer = True

        else:
            self.selling_price = self.actual_price
            self.is_offer = False
            self.discount_price = 0

        if self.stock == 0:
            self.in_stock = False
            if self.discounted_percentage:
                self.selling_price = self.actual_price
                self.is_offer = False
                self.discount_price = 0
                self.discounted_percentage = 0
        else:
            self.in_stock = True
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name


    def count_review(self):
        return ProductMessage.objects.filter(review__product = self.uid).count()


class ProductImages(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    product_image = models.ImageField(upload_to='products')


class ProductReview(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_product')

    def __str__(self) -> str:
        return self.product.product_name


class ProductMessage(BaseModel):
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name='review')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.review.product.product_name

class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

    def __str__(self) -> str:
        return self.coupon_code

    


