from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register
class GhostArticleDetailApphook(CMSApp):
    name = _("Ghost article detail")
    app_name = "ghost_article_detail"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["djangocms_pai_ghost_articles.urls"]
