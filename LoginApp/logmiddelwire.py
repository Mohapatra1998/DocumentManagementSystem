from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRedirectMiddleware(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "AdminApp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admindashboard"))
            elif user.user_type == "2":
                if modulename == "ManagerApp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("managerdashboard"))
            elif user.user_type == "3":
                if modulename == "UserApp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse('userdashboard'))

            else:
                return HttpResponseRedirect(reverse("login"))

        else:
            if modulename == "LoginApp.views" or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("login"))