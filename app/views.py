from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.views.generic import TemplateView
# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super().get_context_data()
        if self.request.GET:
            base_url = "http://www.nfl.com/players/search?category=name&filter={}&playerType={}"
            data = requests.get(base_url.format(self.request.GET.get('player_name'), self.request.GET.get('playerType')))
            souper = BeautifulSoup(data.text, "html.parser")
            table = souper.find('table', {'class': 'data-table1'})
            all_a_tags = table.findAll('a')[::2]
            urls = []
            for result in all_a_tags:
                urls.append(result.get('href'))
            print(urls)
            context['url_links'] = urls
        return context
