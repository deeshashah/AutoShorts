from .forms import UserForm
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators import csrf
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
import json
from summa import summarizer
from bs4 import BeautifulSoup
from scraping.scraper import Scraper
from django.http import JsonResponse
import requests

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def index(request):
	return render(request, 'accounts/index.html')

def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()
            print user
            registered = True
            return HttpResponseRedirect("/dashboard/")

        else:
            print user_form.errors
    else:
        user_form = UserForm()
    
    return render(request,
            'accounts/register.html',
            {'user_form': user_form, 'registered': registered},
            )

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'accounts/login.html', {}, context)


def dashboard(request):
    if request.user.is_authenticated():
        r = requests.get('https://newsapi.org/v1/articles?source=mirror&apiKey=6df0769e0d6244aaa00768c02f123fb2')
        response_dictionary = {}
        response_dictionary["source"] = "mirror"
        data = json.loads(r.text)
        list_of_urls = []
        article_data = []
        main_dict = {}
        i = 0;
        for item in data["articles"]:
            mid_dictionary = {}
            if(type(item["title"])=="unicode"):
                ti = unicodedata.normalize('NFKD', item["title"]).encode('ascii','ignore')
            else : 
                ti = item["title"]
            print ti
            print len(ti)
            n = len(ti)
            if(n >10):
                mid_dictionary["title"] = ti
                sc = Scraper()
                print item
                mid_dictionary["data"] = sc.scrape_mirror(item["url"])
                article_data.append(mid_dictionary)
                mid_dictionary["image"] = (item["urlToImage"])
                print mid_dictionary["image"]
                if(type(mid_dictionary["data"])=="unicode"):
                    st = unicodedata.normalize('NFKD', mid_dictionary["data"]).encode('ascii','ignore')
                else:
                    st = mid_dictionary["data"]

                try:
                        
                    print "********Summary******"
                    summary = summarizer.summarize(st,words=50)
                    print summary.encode('ascii', 'ignore') 
                    print "---------Summary---------"
                    mid_dictionary["summary"] = summarizer.summarize(st,words=50)
                except ZeroDivisionError:
                    mid_dictionary["summary"] = st

                print mid_dictionary
                main_dict["article_"+str(i)] = mid_dictionary
                i = i+1
            
        
        response_dictionary["articles"] = article_data
        
        print main_dict
        for key,value in main_dict.iteritems():
            print "***************"
        
        return render(request,
                'accounts/dashboard.html',
                {'main_dict': main_dict}
                )
    else:
         return HttpResponseRedirect("/login")

