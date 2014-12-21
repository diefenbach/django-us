from django.http import Http404

import pytest

import us.views
from us.models import Url


@pytest.mark.unit_test
@pytest.mark.django_db
def test_redirect_404(gr):
    with pytest.raises(Http404) as e:
        us.views.redirect_to_url(gr, "404")
    assert e.typename == "Http404"


@pytest.mark.unit_test
@pytest.mark.django_db
def test_redirect(gr):
    Url.objects.create(short_url="iq", url="http://www.iqpp.de")
    response = us.views.redirect_to_url(gr, "iq")
    assert response.status_code == 302


@pytest.mark.unit_test
@pytest.mark.django_db
def test_add_url_get(gr, user_with_perm):
    gr.user = user_with_perm
    response = us.views.add_url(gr)
    assert response.status_code == 200
    assert "id_short_url" in response.content
    assert "id_url" in response.content
    assert "id_override" in response.content


@pytest.mark.unit_test
@pytest.mark.django_db
def test_add_url_post_missing_url(pr, user_with_perm):
    assert Url.objects.count() == 0

    pr.user = user_with_perm
    response = us.views.add_url(pr)
    assert response.status_code == 200
    assert "This field is required." in response.content
    assert Url.objects.count() == 0


@pytest.mark.unit_test
@pytest.mark.django_db
def test_add_url_post_valid(pr, user_with_perm):
    assert Url.objects.count() == 0

    pr.POST = {
        "short_url": "iq",
        "url": "http://www.iqpp.de",
    }
    pr.user = user_with_perm
    response = us.views.add_url(pr)
    assert response.status_code == 200
    assert Url.objects.count() == 1

    url = Url.objects.get(short_url="iq")
    assert url.url == "http://www.iqpp.de"


@pytest.mark.unit_test
@pytest.mark.django_db
def test_add_url_post_missing_short_url(pr, user_with_perm):
    assert Url.objects.count() == 0

    pr.POST = {
        "url": "http://www.iqpp.de",
    }
    pr.user = user_with_perm
    response = us.views.add_url(pr)
    assert response.status_code == 200
    assert Url.objects.count() == 1

    url = Url.objects.get(url="http://www.iqpp.de")
    assert len(url.short_url) == 4


@pytest.mark.unit_test
@pytest.mark.django_db
def test_add_url_post_already_exists(pr, user_with_perm):
    assert Url.objects.count() == 0

    pr.POST = {
        "url": "http://www.iqpp.de",
        "short_url": "iq",
    }
    pr.user = user_with_perm
    response = us.views.add_url(pr)
    assert response.status_code == 200
    assert Url.objects.count() == 1

    response = us.views.add_url(pr)
    assert response.status_code == 200
    assert "Url with this Short URL already exists: http://www.iqpp.de" in response.content
    assert Url.objects.count() == 1

    pr.POST = {
        "url": "http://www.iqpp-2.de",
        "short_url": "iq",
        "override": True,
    }

    response = us.views.add_url(pr)
    assert response.status_code == 200
    assert Url.objects.count() == 1


@pytest.mark.unit_test
@pytest.mark.django_db
def test_url_model():
    url = Url.objects.create(url="http://www.iqpp.de", short_url="iq")
    assert url.__unicode__() == "iq -> http://www.iqpp.de"
