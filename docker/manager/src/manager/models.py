import logging
import uuid

from django.db import models
from django.utils.text import slugify


logger = logging.getLogger(__name__)


def dirty_image_path(instance, filename):
    return '%s/%s' % ("dirty_images", filename)


def new_uid():
    return uuid.uuid4().hex


class Feed(models.Model):
    name = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, unique=True, null=True)
    uid = models.CharField(
        max_length=255, 
        default=new_uid
    )
    url = models.CharField(max_length=255, null=True)
    streak_limit = models.IntegerField(default=5)
    max_images = models.IntegerField(default=15)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Feed"
        verbose_name_plural = "Feeds"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Blog(models.Model):
    uid = models.CharField(max_length=255, default=new_uid)
    url = models.URLField(max_length=255, null=True, unique=True)
    name = models.CharField(max_length=255, null=True, unique=True)
    slug = models.CharField(max_length=255, null=True, unique=True)
    # TO DO later
    tags = models.ManyToManyField('manager.BlogTag', blank=True)
    images = models.ManyToManyField('manager.DirtyImage', blank=True)
    categories = models.ManyToManyField('manager.Category', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @classmethod
    def cook_blog(cls, **data):
        try:
            blog = cls(**data)
            blog.save()
        except Exception as error:
            logger.error(str(error))
            return False, str(error)
        return True, blog

    @classmethod
    def get_blogs_data(cls):
        return [
            {"name" : i.name, "url" : i.url} for i in cls.objects.all()
        ]


class Category(models.Model):
    uid = models.CharField(max_length=255, default=new_uid)
    name = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
   

class BlogTag(models.Model):
    uid = models.CharField(max_length=255, default=new_uid)
    name = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DirtyImage(models.Model):
    uid = models.CharField(max_length=255, default=new_uid)
    image = models.ImageField(upload_to=dirty_image_path)
    name = models.CharField(max_length=255, null=True)
    parent_blog = models.ForeignKey(
        'manager.Blog', 
        on_delete=models.CASCADE,    
        null=True
    )
    is_published = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Dirty Image"
        verbose_name_plural = "Dirty Images"

    def __str__(self):
        return "%s - %s" % (
            self.pk,
            self.image.path
        )

    @classmethod
    def image_exists(cls, name):
        if cls.objects.filter(name=name).exists():
            return True
        return False


class ScrapeLog(models.Model):
    blog = models.ForeignKey('manager.Blog', on_delete=models.CASCADE, null=True)
    uid = models.CharField(max_length=255, default=new_uid)
    created_at = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(default=dict)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Scrape Log"
        verbose_name_plural = "Scrapes Logs"
    
    def __str__(self):
        return "Scrape record for %s on %s" % (
            self.blog.name, 
            self.created_at
        )

    @classmethod
    def cook_scrape(cls, uid, meta):
        try:
            obj = cls.objects.create(
                blog=Blog.objects.get(uid=uid),
                meta=meta
            )
        except Exception as error:
            logger.info(str(error))
            return False, None
        return True, obj
    
    @classmethod
    def cook_multiple_scrapes(cls, uids, data):
        data = data.get('scrapes_data', None)
        # handle error responses.
        if data is None:
            for each in uids:
                cls.objects.create(
                    uid,
                    meta={
                        'error' : data
                    }
                )
            return False
        # handle success response.
        for each in data:
            cls.cook_scrape(
                each["blog_uid"], 
                {
                    'scrape_data' : each
                }
            )
        return True

    @property
    def verdict(self):
        if self.meta.get('scrape_data', None) is not None:
            return self.meta.get('scrape_data').get('success')
        return False
    
    @property
    def start_time(self):
        if self.meta.get("scrape_data", None) is not None:
            return self.meta["scrape_data"].get(
                    'times',
                    {}
                ).get(
                    "start_time", 
                    "-no start time-"
                )
        return "-no start time available for this scrape-"
    
    @property
    def end_time(self):
        if self.meta.get("scrape_data", None) is not None:
            return self.meta["scrape_data"].get(
                    "times", 
                    {}
                ).get(
                    "end_time", 
                    "-no end time-"
                )
        return "-no end time available for this scrape-"
    
    @property
    def get_readable_summary(self):
        return """
        Scrape for %s was a %s. Start time was %s and end time was %s
        """ % (
            self.blog.name,
            "success" if self.verdict else "failure", 
            self.start_time, 
            self.end_time
        )


class BdsmlrCredentials(models.Model):
    email = models.EmailField(max_length=255, null=True, unique=True)
    password = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    slug = models.CharField(max_length=255, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Bdsmlr Credential"
        verbose_name_plural = "Bdsmlr Credentials"
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
