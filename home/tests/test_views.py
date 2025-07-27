from django.urls import reverse 
from django.test import TestCase , Client
from home.models import Episode , Course
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile # making fake images for our testing 

class TestHomeView(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_home_view_no_args(self):
        response = self.client.get(reverse("home:home"))
        self.assertTemplateUsed(response,"home/home.html")
        self.assertEqual(list(response.context["episodes"]), list(Episode.objects.all()))
        self.assertEqual(list(response.context["courses"]), list(Course.objects.all()))
        self.assertEqual(response.status_code , 200)

    def test_home_view_with_args(self):
        fake_image = SimpleUploadedFile(name="test.jpg",content=b"file_content",content_type="image/jpg")
        course = baker.make(Course , slug= "django", image=fake_image)
        episode = baker.make(Episode, course=course)
        response = self.client.get(reverse("home:episodes" , kwargs={"course_slug":course.slug}))

        self.assertEqual(list(response.context["courses"]) , list(Course.objects.all()))
        self.assertEqual(list(response.context["episodes"]),list(Episode.objects.filter(course=course)))
        self.assertTemplateUsed(response,"home/home.html")
        self.assertEqual(response.status_code , 200)
        self.assertIn(episode , response.context["episodes"])


class TestVideoDetailView(TestCase):

    def setUp(self):
        self.client = Client()
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