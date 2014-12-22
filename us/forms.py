from django import forms
from django.utils.translation import ugettext_lazy as _
from us.models import Url


class UrlForm(forms.ModelForm):
    """
    Form to add new URL.

    Checks whether an short URL is already existing.
    """
    override = forms.BooleanField(label=_(u"Override"), required=False)

    class Meta:
        model = Url

    def __init__(self, *args, **kwargs):
        super(UrlForm, self).__init__(*args, **kwargs)
        self.fields["short_url"].required = False

    def clean(self):
        override = self.cleaned_data.get("override")
        short_url = self.cleaned_data.get("short_url", "")

        if short_url != "":
            try:
                url = Url.objects.get(short_url=short_url)
            except Url.DoesNotExist:
                pass
            else:
                if not override:
                    self.add_error("short_url", _("Url with this Short URL already exists: {url}".format(url=url.url)))

        return self.cleaned_data
