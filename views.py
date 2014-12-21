import random
import string

from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from us.forms import UrlForm
from us.models import Url


def redirect_to_url(request, short_url):
    """
    Redirects the user to the url which is stored for the short url.
    """
    try:
        url = Url.objects.get(short_url=short_url)
    except Url.DoesNotExist:
        raise Http404()
    else:
        return HttpResponseRedirect(url.url)


@permission_required("us.add_url", login_url="us_login")
def add_url(request, template_name="us/url_form.html"):
    """
    Provides form and logic to add a new url.
    """
    if request.method == "GET":
        form = UrlForm()
    else:
        form = UrlForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data.get("short_url").strip() != "":
                new_short_url = form.cleaned_data.get("short_url")
            else:
                while 1:
                    new_short_url = ''.join(random.choice(string.ascii_letters) for _ in range(4))
                    try:
                        Url.objects.get(short_url=new_short_url)
                    except Url.DoesNotExist:
                        break

            url, created = Url.objects.get_or_create(
                short_url=new_short_url,
            )

            url.url = form.cleaned_data.get("url")
            url.save()

            return HttpResponse(url.short_url)

    return render_to_response(template_name, RequestContext(request, {
        "form": form,
    }))
