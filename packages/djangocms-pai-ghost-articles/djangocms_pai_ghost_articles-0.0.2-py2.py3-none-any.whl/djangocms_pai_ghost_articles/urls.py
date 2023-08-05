from django.conf.urls import url

from .views import GhostArticleDetailView


urlpatterns = [

    url(r'^(?P<path>.*)/$', GhostArticleDetailView.as_view(), name='ghost_article_detail'),
]
