import re
from django.core.urlresolvers import reverse
import pytest


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
