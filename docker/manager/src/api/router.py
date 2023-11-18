from django.urls import path
from rest_framework.routers import DefaultRouter
from api.endpoints import (
    blog_endpoints, 
    feed_endpoints, 
    image_endpoints,
    tag_endpoints
)

app_name = "api"

######################################
# Routers
######################################

api_router = DefaultRouter()
api_router.register(
    r'blogs',
    blog_endpoints.BlogViewset,
    basename='blogs'
)
api_router.register(
    r'tags',
    tag_endpoints.BlogTagsViewset,
    basename='tags'
)
api_router.register(
    r'images',
    image_endpoints.ImagesViewset,
    basename='images'
)
#######################################
# URLPATTERNS
#######################################

urlpatterns = [
    path(
        'feed/get-feed-stats',
        view=feed_endpoints.FeedStats.as_view(),
        name='get-feed-stats'
    ),
    path(
        'feed/set-env-status/<status>',
        view=feed_endpoints.EnvSwitch.as_view(),
        name='set-env-status'
    ),
    path(
        'feed/get-feed-credentials',
        view=feed_endpoints.LoadManagerCredentials.as_view(),
        name='get-feed-credentials'
    )
]

urlpatterns += api_router.urls
