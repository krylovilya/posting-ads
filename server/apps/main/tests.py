from django.contrib.auth.models import Group, User
from django.test import Client, TestCase

import pytest

from apps.main.models import Ad, Category


class ViewsTestCase(TestCase):
    """Tests for django.test.TestCase"""

    def setUp(self):
        Group.objects.create(name='common users')
        self.user = User.objects.create_user(username='test_user', email='test@user.com')
        self.client = Client()
        self.client.force_login(self.user)
        self.category = Category.objects.create(title='test_category')
        self.ad = Ad.objects.create(
            title='test_ad',
            category_id=self.category.id,
            seller_id=self.user.seller.id
        )

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'main/error_page.html')

    def test_ads_list_view(self):
        response = self.client.get('/ads/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'main/error_page.html')

    def test_ad_detail_view(self):
        response = self.client.get(f'/ads/{self.ad.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'main/error_page.html')

    def test_seller_update_view(self):
        response = self.client.get('/accounts/seller/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'main/error_page.html')

    def test_seller_update_view_anonymous(self):
        self.client.logout()
        response = self.client.get('/accounts/seller/')
        self.assertTemplateNotUsed(response, 'main/error_page.html')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/seller/')

    def test_ad_create_view(self):
        response = self.client.get('/ads/add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'main/error_page.html')

    def test_ad_update_view(self):
        response = self.client.get(f'/ads/{self.ad.id}/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'main/error_page.html')

    def test_ad_update_view_anonymous(self):
        self.client.logout()
        response = self.client.get(f'/ads/{self.ad.id}/edit/')
        self.assertRedirects(response, f'/accounts/login/?next=/ads/{self.ad.id}/edit/')


# tests for pytest


@pytest.fixture
def set_up():
    Group.objects.create(name='common users')
    user = User.objects.create_user(username='test_user', email='test@user.com')
    client = Client()
    client.force_login(user)
    category = Category.objects.create(title='test_category')
    ad = Ad.objects.create(
        title='test_ad',
        category_id=category.id,
        seller_id=user.seller.id
    )
    return {
        'user': user,
        'client': client,
        'category': category,
        'ad': ad
    }


@pytest.mark.django_db
def test_index_view(set_up):
    response = set_up['client'].get('/')
    assert response.status_code == 200
    assert 'main/error_page.html' not in (t.name for t in response.templates)


@pytest.mark.django_db
def test_ads_list_view(set_up):
    response = set_up['client'].get('/ads/')
    assert response.status_code == 200
    assert 'main/error_page.html' not in (t.name for t in response.templates)


@pytest.mark.django_db
def test_ad_detail_view(set_up):
    ad = set_up['ad']
    response = set_up['client'].get(f'/ads/{ad.id}/')
    assert response.status_code == 200
    assert 'main/error_page.html' not in (t.name for t in response.templates)


@pytest.mark.django_db
def test_seller_update_view(set_up):
    response = set_up['client'].get('/accounts/seller/')
    assert response.status_code == 200
    assert 'main/error_page.html' not in (t.name for t in response.templates)


@pytest.mark.django_db
def test_seller_update_view_anonymous(set_up):
    client = set_up['client']
    client.logout()
    response = client.get('/accounts/seller/')
    assert 'main/error_page.html' not in (t.name for t in response.templates)
    assert response.url == '/accounts/login/?next=/accounts/seller/'
    assert response.status_code == 302


@pytest.mark.django_db
def test_ad_create_view(set_up):
    response = set_up['client'].get('/ads/add/')
    assert response.status_code == 200
    assert 'main/error_page.html' not in (t.name for t in response.templates)


@pytest.mark.django_db
def test_ad_update_view(set_up):
    ad = set_up['ad']
    response = set_up['client'].get(f'/ads/{ad.id}/edit/')
    assert response.status_code == 200
    assert 'main/error_page.html' not in (t.name for t in response.templates)


@pytest.mark.django_db
def test_ad_update_view_anonymous(set_up):
    client = set_up['client']
    client.logout()
    ad = set_up['ad']
    response = client.get(f'/ads/{ad.id}/edit/')
    assert response.url == f'/accounts/login/?next=/ads/{ad.id}/edit/'
    assert response.status_code == 302


def test_robots_txt_get():
    client = Client()
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response["content-type"] == "text/plain"
    lines = response.content.decode().splitlines()
    assert lines[0] == "User-Agent: *"


def test_robots_txt_post_disallowed():
    client = Client()
    response = client.post("/robots.txt")
    assert response.status_code == 405
