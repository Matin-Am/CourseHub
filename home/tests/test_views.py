from django.urls import reverse 
from django.test import TestCase , Client
from django.core.files.uploadedfile import SimpleUploadedFile # making fake images for our testing 
from accounts.models import User
from home.models import Episode , Course
from model_bakery import baker


class TestHomeView(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse("home:home"))
        self.assertTemplateUsed(response,"home/home.html")
        self.assertEqual(list(response.context["courses"]), list(Course.objects.all()))
        self.assertEqual(response.status_code , 200)

class TestVideoDetailView(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username="test",email="test@email.com",password="test")
        self.client.force_login(user)
        self.fake_image = SimpleUploadedFile(name="test.jpg",content=b"file_content",content_type="image/jpg")
        self.fake_video = SimpleUploadedFile(name="test.mp4",content=b"file_content",content_type="video/mp4")

    def test_paid_video_detail(self):
       
        course = baker.make(Course ,image=self.fake_image , paid=True )
        episode = baker.make(Episode ,slug = "django" , video=self.fake_video , course=course)
        response = self.client.get(reverse("home:video", kwargs={"epi_slug":"django"}))
        self.assertEqual(response.status_code , 200)
        self.assertTemplateUsed(response, "home/detail.html")
        self.assertEqual(response.context["episode"],episode)

  
    def test_unpaid_video_detail(self):
        course = baker.make(Course , image=self.fake_image , paid=False)
        episode = baker.make(Episode ,slug = "django" , video=self.fake_video , course=course)
        response = self.client.get(reverse("home:video", kwargs={"epi_slug":"django"}))
        self.assertEqual(response.status_code , 302)
        self.assertRedirects(response,reverse("home:home"))