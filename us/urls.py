from django.conf.urls import patterns, url

urlpatterns = patterns('django.contrib.auth.views',
    url('^login', "login", {"template_name": "us/login.html"}, name='us_login'),
    url('^logout', "logout", {"template_name": "us/logged_out.html"}, name='us_logout'),
)

urlpatterns += patterns('us.views',
    url(r'^add-url-form$', "add_url_form", name='us_add_url_form'),
    url(r'^add-url$', "add_url", name='us_add_url'),
    url(r'^(?P<short_url>\w+)$', "redirect_to_url", name='us_redirect_to_url'),
)
