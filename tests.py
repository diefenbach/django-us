import re

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse

import pytest
from selenium import webdriver


BROWSERS = {
    # 'firefox': webdriver.Firefox,
    # 'chrome': webdriver.Chrome,
    'phantomjs': webdriver.PhantomJS,
}


# Fixtures
@pytest.fixture(scope="session", params=BROWSERS.keys())
def browser(request):
    browser = BROWSERS[request.param]()
    request.addfinalizer(lambda *args: browser.quit())
    return browser


@pytest.fixture(scope="function")
def user():
    user = User.objects.create_user('doe', 'john@doe.com', 'pw')
    return user


@pytest.fixture(scope="function")
def user_with_perm(user):
    add_url = Permission.objects.get(codename="add_url")
    user.user_permissions.add(add_url)
    return user


# Fixture tests
@pytest.mark.django_db
def test_user_fixture(user):
    assert user.username == "doe"
    assert user.has_perm("us.add_url") is False

    add_url = Permission.objects.get(codename="add_url")
    user.user_permissions.add(add_url)

    delattr(user, "_perm_cache")  # wtf?
    assert user.has_perm("us.add_url") is True


@pytest.mark.django_db
def test_user_with_perm_fixture(user_with_perm):
    assert user_with_perm.username == "doe"
    assert user_with_perm.has_perm("us.add_url") is True


# Browser tests
@pytest.mark.browser_test
def test_add_url(browser, user_with_perm, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)
    _login(browser)
    short_url = browser.find_element_by_name("short_url")
    short_url.send_keys("test")
    url = browser.find_element_by_name("url")
    url.send_keys("http://www.test.de")
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "test" in browser.page_source


@pytest.mark.browser_test
def test_add_url_missing_all_fields(browser, user_with_perm, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)
    _login(browser)
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "This field is required." in browser.page_source


@pytest.mark.browser_test
def test_add_url_missing_url_field(browser, user_with_perm, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)

    # login
    u = browser.find_element_by_name("username")
    u.send_keys("doe")
    p = browser.find_element_by_name("password")
    p.send_keys("pw")
    b = browser.find_element_by_css_selector("input[type='submit']")
    b.click()

    short_url = browser.find_element_by_name("short_url")
    short_url.send_keys("test")
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "This field is required." in browser.page_source


@pytest.mark.browser_test
def test_add_url_missing_short_url_field(browser, user_with_perm, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)

    # login
    u = browser.find_element_by_name("username")
    u.send_keys("doe")
    p = browser.find_element_by_name("password")
    p.send_keys("pw")
    b = browser.find_element_by_css_selector("input[type='submit']")
    b.click()

    url = browser.find_element_by_name("url")
    url.send_keys("http://www.test.de")
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert re.search(r"<body>\w{4}</body>", browser.page_source)


@pytest.mark.browser_test
def test_add_url_already_existing(browser, user_with_perm, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)

    # login
    u = browser.find_element_by_name("username")
    u.send_keys("doe")
    p = browser.find_element_by_name("password")
    p.send_keys("pw")
    b = browser.find_element_by_css_selector("input[type='submit']")
    b.click()

    short_url = browser.find_element_by_name("short_url")
    short_url.send_keys("test")
    url = browser.find_element_by_name("url")
    url.send_keys("http://www.test.de")
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "test" in browser.page_source

    url = reverse("us_add_url")
    browser.get(live_server.url + url)
    short_url = browser.find_element_by_name("short_url")
    short_url.send_keys("test")
    url = browser.find_element_by_name("url")
    url.send_keys("http://www.test.de")
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "Url with this Short URL already exists" in browser.page_source

    override = browser.find_element_by_name("override")
    override.click()
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "test" in browser.page_source


def _login(browser):
    # login
    u = browser.find_element_by_name("username")
    u.send_keys("doe")
    p = browser.find_element_by_name("password")
    p.send_keys("pw")
    b = browser.find_element_by_css_selector("input[type='submit']")
    b.click()
