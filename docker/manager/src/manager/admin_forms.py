from django import forms

from api.mixins import BlogsMixin
from manager.models import Feed


class AdminBlogForm(BlogsMixin, forms.ModelForm):

    def clean_url(self):
        url = self.cleaned_data["url"]
        exists = self.blog_exists(url)
        if not exists[0]:
            raise forms.ValidationError("Invalid bdsmlr blog.")
        return url


class AdminFeedForm(forms.ModelForm):

    def clean_url(self):
        feed = Feed.objects.all() 
        if feed.count() == 1:
            raise forms.ValidationError(
                (
                    "A feed is already configured: %s. The manager does "
                    "not support multiple feed functionality. "
                    "The existing feed was created when you ran docker-compose up, "
                    "If this feed is not running, check your images by running: "
                    "'docker ps -a'." % feed.first().url
                )
            ) from None
        if self.cleaned_data["url"].endswith("/"):
            raise forms.ValidationError(
                "Feed url should not end with a slash '/' at the end "
            ) from None
        return self.cleaned_data["url"]
        
