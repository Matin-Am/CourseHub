from django.test import TestCase
from django.urls import reverse , resolve
from home.views import HomeView , VideoDetailView


class TestHomeUrls(TestCase):

    def test_home_url(self):
        url =  reverse("home:home")
        self.assertEqual(resolve(url).func.view_class , HomeView )

    def test_video_url(self):
        url = reverse("home:video", kwargs={"epi_slug":"first_episode"})
        self.assertEqual(resolve(url).func.view_class , VideoDetailView)