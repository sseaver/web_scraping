from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from django.views.generic import TemplateView
# Create your views here.


is_current = True


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self):
        context = super().get_context_data()
        if self.request.GET:
            base_url = "http://www.nfl.com/players/search?category=name&filter={}&playerType={}"
            data = requests.get(base_url.format(self.request.GET.get('player_name'), self.request.GET.get('playerType')))
            souper = BeautifulSoup(data.text, "html.parser")
            if self.request.GET.get('playerType') == "current":
                table = souper.find('table', {'class': 'data-table1'})
                all_a_tags = table.find_all('a')[::2]
                urls = [(result.get('href'), result.get_text()) for result in all_a_tags]
                context['url_links'] = urls
                return context
            elif self.request.GET.get('playerType') == "historical":
                table = souper.find('table', {'class': 'data-table1'})
                all_a_tags = table.find_all('a')
                urls = [(result.get('href')+'?historical=True', result.get_text()) for result in all_a_tags]
                context['url_links'] = urls
                return context


class PlayerStatsView(TemplateView):
    template_name = "player_stats.html"

    def get_context_data(self, player_url):
        context = super().get_context_data()
        page = requests.get("http://www.nfl.com/" + player_url)
        souper = BeautifulSoup(page.text, 'html.parser')
        if self.request.GET.get('historical') == "True":
            context['table'] = souper.findAll('table', {'class': 'data-table1'})
            return context
        else:
            context['table'] = souper.findAll('table', {'class': 'data-table1'})[1].contents
            return context
