
'''
session = {
    'course_data':{

        'username':{

            'course':{
                'price':'',
                'add_time': '',
            }

       }
    }
}
'''
from django.utils import timezone
from django.contrib import messages

CART_SESSION_ID = 'course_data'
class Cart:
   
    def __init__(self, request , username, course):

        self.session = request.session
        self.username = username
        self.course = course

        if 'course_data' not in self.session:
            self.session['course_data'] = {}

        if username not in self.session['course_data']:
            self.session['course_data'][username] = {}

        if str(course) not in self.session['course_data'][username]:
            self.session['course_data'][username][str(course)] = {}

        
    def add(self,request):
        self.session['course_data'][self.username][str(self.course)] = {
            "price":str(self.course.price) , 
            'add_time': str(timezone.now())}
        self.save()

    def save(self):
        self.session.modified = True