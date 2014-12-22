from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

import pytest
from selenium import webdriver


BROWSERS = {
    'firefox': webdriver.Firefox,
    # 'chrome': webdriver.Chrome,
    # 'phantomjs': webdriver.PhantomJS,
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


@pytest.fixture(scope="function")
def gr(rf):
    return rf.get("/")


@pytest.fixture(scope="function")
def pr(rf):
    return rf.post("/")
