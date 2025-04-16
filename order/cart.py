
'''
session = {
    'course_data':{

        'username':{

            'course_slug':{
                'price':'',
                'add_time': '',
            }

       }
    }
}
'''
from django.utils import timezone
from home.models import Course

CART_SESSION_ID = 'course_data'
class Cart:
   
    def __init__(self, request , username, course_slug=None): # we use course_slug just for add() method 

        self.session = request.session
        self.username = username
        self.course_slug = course_slug

        if CART_SESSION_ID not in self.session:
            self.session[CART_SESSION_ID] = {}

        if username not in self.session[CART_SESSION_ID]:
            self.session[CART_SESSION_ID][username] = {}

        if course_slug and course_slug not in self.session[CART_SESSION_ID][username]:
            self.session[CART_SESSION_ID][username][course_slug] = {}

        
    def add(self,request):
        course = Course.objects.get(slug=self.course_slug)
        self.session[CART_SESSION_ID][self.username][self.course_slug] = {
            "price":str(course.price) , 
            'add_time': str(timezone.now())}
        self.save()


    def get_total_price(self):
        return sum(int(item["price"]) for item in self.session[CART_SESSION_ID][self.username].values())


    def __iter__(self):
        cart_data = self.session[CART_SESSION_ID][self.username]
        courses = Course.objects.filter(slug__in=cart_data.keys())

        
        for course in courses:
            cart = cart_data[course.slug].copy()
            cart['course'] = course
            yield cart

    def __len__(self):
        return len([item for item in self.session[CART_SESSION_ID][self.username]])



    def remove(self):
        del self.session[CART_SESSION_ID][self.username][self.course_slug]
        self.save()



    def save(self):
        self.session.modified = True