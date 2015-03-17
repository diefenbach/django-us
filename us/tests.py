from django.core.urlresolvers import reverse

import pytest
from selenium import webdriver


BROWSERS = {
    'firefox': webdriver.Firefox,
    # 'chrome': webdriver.Chrome,
}


@pytest.fixture(scope="session", params=BROWSERS.keys())
def browser(request):
    browser = BROWSERS[request.param]()
    request.addfinalizer(lambda *args: browser.quit())
    return browser


@pytest.mark.browser_test
def test_add_url(browser, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)
    short_url = browser.find_element_by_name("short_url")
    short_url.send_keys("test")
    url = browser.find_element_by_name("url")
    url.send_keys("http://www.test.de")
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "test" in browser.page_source


@pytest.mark.browser_test
def test_add_url_missing_all_fields(browser, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "This field is required." in browser.page_source


@pytest.mark.browser_test
def test_add_url_missing_url_field(browser, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)
    short_url = browser.find_element_by_name("short_url")
    short_url.send_keys("test")
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "This field is required." in browser.page_source


@pytest.mark.browser_test
def test_add_url_missing_short_url_field(browser, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)
    url = browser.find_element_by_name("url")
    url.send_keys("http://www.test.de")
    submit = browser.find_element_by_css_selector("input[type=submit]")
    submit.click()
    assert "This field is required." in browser.page_source


@pytest.mark.browser_test
def test_add_url_already_existing(browser, live_server):
    url = reverse("us_add_url")
    browser.get(live_server.url + url)
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
