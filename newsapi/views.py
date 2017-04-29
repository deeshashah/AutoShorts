from django.shortcuts import render
import requests
import json
from bs4 import BeautifulSoup
from scraping.scraper import Scraper
from django.http import JsonResponse
from summa import summarizer


def latestnews(request):
	r = requests.get('https://newsapi.org/v1/articles?source=mirror&apiKey=6df0769e0d6244aaa00768c02f123fb2')
	response_dictionary = {}
	# response_dictionary["status"] = r
	response_dictionary["source"] = "mirror"
	data = json.loads(r.text)
	# print data["articles"]
	list_of_urls = []
	article_data = []
	for item in data["articles"]:
		mid_dictionary = {}
		if(type(item["title"])=="unicode"):
			title = unicodedata.normalize('NFKD', item["title"]).encode('ascii','ignore')
		else : 
			title = item["title"]
		if(len(title) >10):
			mid_dictionary["title"] = item["title"]
			mid_dictionary["url"] = item["url"]
			mid_dictionary["urlToImage"] = item["urlToImage"]
			# print item["url"]
			# print "************"
			sc = Scraper()
			mid_dictionary["data"] = sc.scrape_mirror(item["url"])
			article_data.append(mid_dictionary)

	response_dictionary["articles"] = article_data
	
	# news_dictionary = {}
	
	# # print news_dictionary
	# list_of_urls = []
	# return render(request, 'newslist.html', {'newslist':response_dictionary})
	return JsonResponse(response_dictionary,  content_type="application/json")

