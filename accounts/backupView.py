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
import unicodedata
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def index(request):
	return render(request, 'accounts/index.html')

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            print user
            registered = True
            return HttpResponseRedirect("/dashboard/")

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        

    # Render the template depending on the context.
    return render(request,
            'accounts/register.html',
            {'user_form': user_form, 'registered': registered},
            )

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request,'accounts/login.html', {}, context)


def dashboard(request):
    if request.user.is_authenticated():
        r = requests.get('https://newsapi.org/v1/articles?source=mirror&apiKey=6df0769e0d6244aaa00768c02f123fb2')
        response_dictionary = {}
        # response_dictionary["status"] = r
        response_dictionary["source"] = "mirror"
        data = json.loads(r.text)
        # print data["articles"]
        list_of_urls = []
        article_data = []
        main_dict = {}
        i = 0;
        for item in data["articles"]:
            mid_dictionary = {}
            mid_dictionary["title"] = item["title"]
            #mid_dictionary["url"] = item["url"]
            #mid_dictionary["urlToImage"] = item["urlToImage"]
            sc = Scraper()
            mid_dictionary["data"] = sc.scrape_mirror(item["url"])
            article_data.append(mid_dictionary)
            print type(mid_dictionary["data"])
            if(type(mid_dictionary["data"])=="unicode"):
                st = unicodedata.normalize('NFKD', mid_dictionary["data"]).encode('ascii','ignore')
            else:
                st = mid_dictionary["data"]
            if(len(st)>250):
                print "********Summary******"
                print summarizer.summarize(st,words=50)
                print "---------Summary---------"
                mid_dictionary["summary"] = summarizer.summarize(st,words=50)
            else :
                mid_dictionary["summary"] = st

            mid_dictionary["article_"+str(i)] = mid_dictionary
            i = i+1
        
        response_dictionary["articles"] = article_data
        
        # news_dictionary = {}
        #print main_dict
        for key,value in main_dict.iteritems():
            print "***************"
            # print key
            
            
            print value["title"]
        # # print news_dictionary
        # list_of_urls = []
        # return render(request, 'newslist.html', {'newslist':response_dictionary})
        return render(request,
                'accounts/dashboard.html',
                {'main_dict': main_dict}
                )
    else:
         return HttpResponseRedirect("/login")


    # r = requests.get('https://newsapi.org/v1/articles?source=mirror&apiKey=6df0769e0d6244aaa00768c02f123fb2')
    # response_dictionary = {}
    # # response_dictionary["status"] = r
    # response_dictionary["source"] = "mirror"
    # data = json.loads(r.text)
    # # print data["articles"]
    # list_of_urls = []
    # article_data = []
    # main_dict = {}
    # i = 0;
    # for item in data["articles"]:
    #     mid_dictionary = {}
    #     mid_dictionary["title"] = item["title"]
    #     #mid_dictionary["url"] = item["url"]
    #     #mid_dictionary["urlToImage"] = item["urlToImage"]
    #     sc = Scraper()
    #     mid_dictionary["data"] = sc.scrape_mirror(item["url"])
    #     article_data.append(mid_dictionary)
    #     print "********Summary******"
    #     print summarizer.summarize(mid_dictionary["data"],words=50)
    #     print "---------Summary---------"
    #     main_dict["article_"+str(i)] = mid_dictionary
    #     i = i+1
    
    # response_dictionary["articles"] = article_data
    
    # # news_dictionary = {}
    # #print main_dict
    # for key,value in main_dict.iteritems():
    #     print "***************"
    #     # print key
        
        
    #     print value["title"]
    # # # print news_dictionary
    # # list_of_urls = []
    # # return render(request, 'newslist.html', {'newslist':response_dictionary})
    # return render(request,
    #         'accounts/dashboard.html',
    #         {'main_dict': main_dict}
    #         )
