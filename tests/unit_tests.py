from django.core.urlresolvers import reverse
from django.http import Http404

import pytest

import us.views
from us.models import Url


@pytest.mark.unit_test
@pytest.mark.django_db
def test_redirect_404(gr):
    with pytest.raises(Http404):
        response = us.views.redirect_to_url(gr, "404")
        assert response.status_code == 404


@pytest.mark.unit_test
@pytest.mark.django_db
def test_redirect(gr):
    Url.objects.create(short_url="iq", url="http://www.iqpp.de")
    response = us.views.redirect_to_url(gr, "iq")
    assert response.status_code == 302
