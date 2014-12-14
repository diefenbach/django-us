from django.conf.urls import patterns, url


urlpatterns = patterns('us.views',
    url(r'^add$', "add_url", name='us_add_url'),
    url(r'^(?P<short_url>\w+)$', "redirect_to_url", name='us_redirect_to_url'),
)
