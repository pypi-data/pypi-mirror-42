import requests
import json
from django.views.generic import TemplateView
from django.http import Http404
from meta.views import Meta


class GhostArticleDetailView(TemplateView):
    template_name = 'ghost/article_detail.html'
    
    def get_article(self, article_slug):
        search_url = 'http://elasticsearch.blinkup.it/ghost_vinievino/_search'
        search_obj = {
          "from" : 0,
          "size" : 1,
          "query": { 
            "bool": { 
              "must": [
                    {
                    "match": {
                        "doc.slug.keyword": article_slug
                      }
                  }
              ]
            }
          },
          "_source": [
              "doc.id",
              "doc.title",
              "doc.feature_image",
              "doc.featured",
              "doc.published_at",
              "doc.html",
              "doc.slug",
              "doc.status",
              "doc.authors.slug",
              "doc.authors.name", 
              "doc.tags.slug",
              "doc.tags.name"
            ]
        }

        print('SEARCHing!!', search_obj)
        resp = requests.post(search_url, json=search_obj)
        resp_obj = resp.json()
        
        article_found = resp_obj['hits']['total'] > 0
        
        if article_found:
            print('SEARCH result:', resp.status_code)
        else:
            raise Http404("Not found.")
        
        article = resp_obj['hits']['hits'][0]['_source']['doc']
        
        print('ARTICLE', article)
        return article

    def get_context_data(self, **kwargs):
        context = super(GhostArticleDetailView, self).get_context_data(**kwargs)
        
        article_slug = context['view'].kwargs['path']
        print('\n\nLooking for ghost article', article_slug)
        
        retries = 0
        try:
            article = self.get_article(article_slug)
        except:
            if retries < 3:
                article = self.get_article(article_slug)
                retries += 1
            else:
                raise
        
        meta = Meta(
            object_type='Article',
            title=article['title'],
            image=article['feature_image']
        )
        
        context['article'] = article
        context['meta'] = meta

        return context
