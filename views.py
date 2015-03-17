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
    """
    try:
        url = Url.objects.get(short_url=short_url)
    except Url.DoesNotExist:
        raise Http404("Redirect to URL")
    else:
        return HttpResponseRedirect(url.url)


# @permission_required("us.add_url")
def add_url(request, template_name="us/url_form.html"):
    """
    Provides form and logic to add a new url.
    """
    if request.method == "GET":
        form = UrlForm()
    else:
        form = UrlForm(data=request.POST)
        if form.is_valid():
            url, created = Url.objects.get_or_create(
                short_url=form.cleaned_data.get("short_url"),
            )
            url.url = form.cleaned_data.get("url")
            url.save()
            return HttpResponse(url.short_url)

    return render_to_response(template_name, RequestContext(request, {
        "form": form,
    }))
