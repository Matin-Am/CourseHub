from django.contrib.auth.mixins import UserPassesTestMixin



class SessionAvailableMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.session['course_data'][self.request.user.username]