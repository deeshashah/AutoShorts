from django.conf.urls import url
from . import views

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    # url(r'^category/(?P<category_name_url>\w+)$', views.category, name='category'),
    # url(r'^add_category/$', views.add_category, name='add_category'),
    # url(r'^category/(?P<category_name_url>\w+)/add_page/$', views.add_page, name='add_page'),
    url('dashboard/$', views.dashboard, name='dashboard'),

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.logout_page, name='logout_page'),
    


]

