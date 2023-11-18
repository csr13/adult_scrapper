import json
import os
import threading

import requests
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

from api.connectors import FeedConnector
from manager.models import (
    Blog, 
    BdsmlrCredentials,
    Category, 
    DirtyImage,
    Feed,
    BlogTag,
    ScrapeLog
)
from manager.admin_forms import AdminBlogForm, AdminFeedForm


@admin.register(Feed)
class AdminFeed(admin.ModelAdmin):
    form = AdminFeedForm
    list_display = [
        "pk",
        "uid",
        "name",
    ]
    exclude = ["status", "streak_limit", "max_images"] 
    prepopulated_fields = {"slug" : ["name"]}
    readonly_fields = ["feed_data"]

    def feed_data(self, obj):
        url = "%s/%s" % (obj.url, "env-stats")
        try:
            resp = requests.get(url)
        except Exception as error:
            return mark_safe(
                "<pre><code>No stats available</code></pre>"
            )
        if resp.status_code != 200:
            return mark_safe(
                "<pre><code>No stats available</code></pre>"
            )
        else:
            if not obj.status:
                obj.status = True
                obj.save()

        data = json.dumps(resp.json())
        try:
            data = self.generate_feed_data_html(resp.json())
        except Exception as error:
            logger.info(str(error))
            data = "<pre><code>No stats available</code></pre>"

        return mark_safe(data)
        
    def generate_feed_data_html(self, data):
        """
        For some reason styles are not usable as generated html,
        reason why html is styled directly.
        """
        env = data["data"]["env"]
        html_blob = """
        <div>
          <h2>
            <bold>Status:</bold>
            <span style='padding: 5px; color: %s; background: %s'>%s</span>
          </h2>
        </div>
        <p></p>
        <p></p>
        """ % (
            "white",
            "red" if not env["on"] else "green",
            "Online" if env["on"] else "Offline"
        )

        html_blob += """
        <div><h2>Loaded Blogs</h2></div>
        <table style='border: 1px solid black'>
          <thead>
            <tr style='%s'>
              <td style='border:1px solid black; text-align: left;'>Name</td></td>
              <td style='border:1px solid black; text-align: left;'>URL</td>
              <td style='border:1px solid black; text-align: left;'>Categories</td>
              <td style='border:1px solid black; text-align: left;'>Created At</td>
            <tr>
            </thead>
            <tbody>
        """
        for blog in env["loaded_blogs"]:
            blog = env["loaded_blogs"][blog]
            html_blob +="""
            <tr>
              <td style='border:1px solid black; text-align: left;'>%s</td>
              <td style='border:1px solid black; text-align: left;'>%s</td>
              <td style='border:1px solid black; text-align: left;'>%s</td>
              <td style='border:1px solid black; text-align: left;'>%s</td>
            </tr>
            """ % (
                blog["name"].capitalize(),
                blog["url"],
                ", ".join(blog["categories"]),
                blog["created_at"]
            )
        html_blob += "</tbody></table>" # closes blogs table 

        try:
            blog_runs = env["runs"]["blog_runs"]
        except KeyError:
            pass
        else:
            html_blob += "<p></p>" * 2
            html_blob += """
            <div><h2>Scrape Log</h2></div>
            <table style='border: 1px solid black'>
              <thead>
                <tr style='%s'>
                    <td style='border:1px solid black; text-align: left;'>Name</td></td>
                    <td style='border:1px solid black; text-align: left;'>URL</td>
                    <td style='border:1px solid black; text-align: left;'>UID</td>
                    <td style='border:1px solid black; text-align: left;'>Start time</td>
                    <td style='border:1px solid black; text-align: left;'>End time</td>
                    <td style='border:1px solid black; text-align: left;'>Verdict</td>
                <tr>
              </thead>
              <tbody>
            """
            for run in blog_runs:
                html_blob += """
                <tr>
                  <td style='border:1px solid black; text-align: left;'>%s</td>
                  <td style='border:1px solid black; text-align: left;'>%s</td>
                  <td style='border:1px solid black; text-align: left;'>%s</td>
                  <td style='border:1px solid black; text-align: left;'>%s</td>
                  <td style='border:1px solid black; text-align: left;'>%s</td>
                  <td style='border:1px solid black; text-align: left;'>%s</td>
                </tr>           
                """ % (
                    run["blog_name"],
                    run["blog_url"],
                    run["blog_uid"],
                    run["times"]["start_time"],
                    run["times"]["end_time"],
                    "Failed" if not run["success"] else "Success"
                )
            html_blob += "</tbody></table>" # closes runs table

        flex = "display: flex; flex-direction: column; margin: 0;" # opens feed data
        generated_html = "<div style='%s'>" % flex
        generated_html += html_blob
        generated_html += "</div>" # closes all html

        return generated_html


@admin.register(DirtyImage)
class AdminDirtyImage(admin.ModelAdmin):
    actions = ["migrate_images_to_site"]
    fieldsets = [
        (
            "Image Data.",
            {
                "fields" : ("name", "uid", "parent_blog"),
                "classes" : ("wide", "extrapretty",),
                "description" : "Basic Image information"
            }
        ),
        (
            "Image Status",
            {
                "fields" : ("is_published",),
                "classes" : ("extrapretty",),
                "description" : (
                    "Indicates whether this image has been migrated to "
                    "remote site"
                )
            }
        ),
        (
            "Image Preview - 18+",
            {
                "fields" : ("image_preview",),
                "classes" : ("collapse", "wide", "extrapretty",),
                "description" : "Preview of the image"
            }
        )
    ]
    list_display = [
        'pk', 
        'is_published',
        'parent_blog',
        'name', 
        'created_at', 
        'media_image_relative_name',
        'image',
    ]
    readonly_fields = ["image_preview"]

    @admin.display(description="Media image relative name")
    def media_image_relative_name(self, obj):
        return obj.image.name.split("/")[1]

    def image_preview(self, obj):
        return mark_safe(
            "<img src='%s' width=%s height=%s />" % (
                obj.image.url,
                obj.image.width,
                obj.image.height
            )
        )

    def migrate_images_to_site(self, request, queryset):
        obj = queryset[0]
        for each in queryset:
            if not os.path.exists(each.image.path):
                continue
    
            parent_blog = each.parent_blog
            image_categories = []
            for category in parent_blog.categories.all():
                image_categories.append(category.name)

            url = "%s/%s" % (
                settings.XXX_SITE_URL, 
                "api/management/image-feed-migrate"
            )
            data = {
                "name" : each.name,
                "categories" : image_categories,
                "blog_data" : {
                    "blog_url" : each.parent_blog.url,
                    "blog_name" : each.parent_blog.name
                }
            }
            resp = requests.post(
                settings.XXX_SITE_URL, 
                data=data, 
                headers={"API-KEY" : settings.XXX_SITE_ADMIN_API_KEY},
                files={"image" : open(each.image.path, "rb")}
            )
            if resp.status_code != 200:
                logger.info("[!] Got resp %s for image %s" % (
                        resp.status_code,
                        each.image
                    )
                )
                continue
                
            each.is_published = True
            each.save()
            continue
            
        messages.info(request, "Images have been migrated!")
        return HttpResponseRedirect(
            reverse(
                "admin:%s_%s_changelist" % (
                    obj._meta.app_label,
                    obj._meta.model_name
                )
            )
        )


@admin.register(Blog)
class AdminBlog(admin.ModelAdmin):
    actions = ["bulk_scrape"]
    form = AdminBlogForm
    fieldsets = [
        (
            "Blog Info",
            {
                "fields" : ("name", "url", "uid", "slug"),
                "classes" : ("extrapretty", "wide",),
                "description" : "Basic blog information."
            }
        ),
        (
            "Blog Details",
            {
                "fields" : ("categories", "tags",),
                "classes" : ("wide", "extrapretty", "collapse",),
                "description" : "Relational information about blog."
            }
        ),
        (
            "Images",
            {
                "fields" : ("images",),
                "classes" : ("wide", "extrapretty", "collapse",),
                "description" : "Images that belong to this blog"
            }
        )
    ]
    list_display = [
        'pk', 
        'uid', 
        'name', 
        'url', 
        'scrape'
    ]
    prepopulated_fields = {"slug" : ("name",)}

    def save_model(self, request, obj, form, change):
        daemon = threading.Thread(
            target=FeedConnector.update_env_blogs,
            kwargs={"delay" : 2}
        )
        daemon.daemon = True
        daemon.start()
        super().save_model(request, obj, form, change)

    def bulk_scrape(self, request, queryset):
        obj = queryset[0]
        uids = [
            x.uid for x in queryset
        ]
        daemon = threading.Thread(
            target=FeedConnector.trigger_bulk_scrape,
            args=(uids,)
        )
        daemon.daemon = True
        daemon.start()
        messages.info(
            request, 
            "Tasks for migration of blogs has been sent to the feed."
        )
        return HttpResponseRedirect(
            reverse(
                "admin:%s_%s_changelist" % (
                    obj._meta.app_label,
                    obj._meta.model_name
                )
            )
        )
    
    @admin.display(description="scrape")
    def scrape(self, instance):
        return mark_safe("<a id='scrape-form-%s' href='%s'>Scrape</a>" % (
                instance.uid, 
                reverse(
                    "manager:single-scrape-admin-action", 
                    args=(instance.uid,)
                )
            )
        )


@admin.register(ScrapeLog)
class AdminScrapeLog(admin.ModelAdmin):
    list_display = [
       "pk",
       "uid",
       "scrape_info",
    ]
    fieldsets = [
        (
            "Scrape Info",
            {
                "fields" : ("blog", "created_at",),
                "classes" : ("wide", "extrapretty",),
                "description" : "Scrape information."
            },
        ),
        (
            "Scrape Details",
            {
                "fields" : (
                    "admin_verdict", 
                    "admin_start_time", 
                    "admin_end_time",
                    "admin_summary",
                ),
                "classes" : ("wide", "extrapretty",),
                "description" : "Scrape meta data."
            }
        ),
        (
            "Raw json meta data",
            {
                "fields" : ("meta",), 
                "classes" : ("wide", "extrapretty", "collapse",),
                "description" : "Raw json meta data returned from feed."
            }
        )
    ]
    readonly_fields = [
        "created_at",
        "admin_verdict",
        "admin_start_time",
        "admin_end_time",
        "admin_summary"
    ]
    
    @admin.display(description="Verdict of the scrape.")
    def admin_verdict(self, obj: ScrapeLog):
        span = """
            <span style='
                background-color: %s; 
                color: white; 
                padding: 5px;
                border: 2px groove white;'>%s
            </span>""" % (
            "red" if not obj.verdict else "green",
            "Scrape completed with no errors" if obj.verdict else (
                "Scrape ran into errors, check raw json for more information"
            )
        )
        return mark_safe(span)
    
    @admin.display(description="Start time of the scrape")
    def admin_start_time(self, obj: ScrapeLog):
        return obj.start_time
    
    @admin.display(description="End time of the scrape")
    def admin_end_time(self, obj: ScrapeLog):
        return obj.end_time
   
    @admin.display(description="Readable summary of the scrape")
    def admin_summary(self, obj: ScrapeLog):
        return obj.get_readable_summary

    @admin.display(description="scrape info")
    def scrape_info(self, instance):
        return instance.__str__()


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = [
        "pk", 
        "uid", 
        "name",
    ]
    fields = [
        "uid",
        "name",
        "slug",
        "images_by_category",
        "images_links",
    ]
    readonly_fields = [
        "images_by_category",
        "images_links"
    ]
    prepopulated_fields = {"slug" : ("name",)}

    def images_by_category(self, obj):
        total_images_by_cat = 0
        blogs_with_cat = Blog.objects.filter(
            categories__slug__exact=obj.slug
        ).aggregate(
            Count("images")
        )
        return "Total images tagged with this category : %s" % (
            blogs_with_cat["images__count"]
        )
    
    @admin.display(description="Images detail links")
    def images_links(self, obj):
        images_links = Blog.objects.filter(
            categories__slug__exact=obj.slug
        ).values("images__name", "images__pk")
        ol = "<div style='margin:0;'><ol>"
        for link in images_links:
            ol += "<li>View in detail ~> <a href='%s'>%s</a></li>" % (
                reverse(
                    "admin:%s_%s_change" % (
                        "manager", 
                        "dirtyimage"
                    ), 
                    args=(link["images__pk"],)
                ),
                link["images__name"]
            )
        ol += "</ol></div>"
        return mark_safe(ol)


@admin.register(BdsmlrCredentials)
class AdminBdsmlrCredentials(admin.ModelAdmin):
    fields = [
        "name",
        "email",
        "password",
        "slug",
        "flagged",
        "created_at",
    ]
    prepopulated_fields = {
        "slug" : ("name",)
    } 
    readonly_fields = ["created_at"]
