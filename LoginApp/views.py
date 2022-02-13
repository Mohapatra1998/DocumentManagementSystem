from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from LoginApp.models import Document, MyUser
from django.views.decorators.csrf import csrf_exempt
from LoginApp.CustomLogin import AuthBackend
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = AuthBackend.authenticate(request, username, password)
        print("#########################################", user)

        if user != None:
            login(request, user)
            if user.user_type == '1':
                messages.success(request, 'Login Successfuly in Admin Panel')
                return HttpResponseRedirect(reverse('admindashboard'))
            if user.user_type == '2':
                messages.success(request, 'Login Successfuly in Manager Panel')
                return HttpResponseRedirect(reverse('managerdashboard'))
            if user.user_type == '3':
                messages.success(request, 'Login Successfuly in User Panel')
                return HttpResponseRedirect(reverse('userdashboard'))
        else:
             messages.error(request, 'This Email and password does not exist any user account, First create a account and login')
             return render(request, 'logintemplates/login.html')
    else:
        return render(request, 'logintemplates/login.html')


def qr_scanner_page(request,id):
    doc = Document.objects.get(id = id)
    drwn_no = doc.file_numble
    return render(request,'logintemplates/qr_scanner.html',{"drwn_no":drwn_no,"doc_id":doc.id})


@csrf_exempt
def scanner_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        doc_id = request.POST.get('doc_id')
        user = AuthBackend.authenticate(request, email, password)
        if user != None:
            if user.user_type== "1":
                login(request,user)
                data={"message":"alogin","doc_id":doc_id}
                return JsonResponse(data,content_type="application/json",safe=False)
            elif user.user_type== "2":
                login(request,user)
                data={"message":"mlogin","doc_id":doc_id}
                return JsonResponse(data,content_type="application/json",safe=False)
            elif user.user_type== "3":
                login(request,user)
                data={"message":"ulogin","doc_id":doc_id}
                return JsonResponse(data,content_type="application/json",safe=False)
        else:
            data={"message":"invalid_credintial"}
            return JsonResponse(data,content_type="application/json",safe=False)
    else:
        data={"message":"invalid Method"}
        return JsonResponse(data,content_type="application/json",safe=False)


































# def user_signup(request):
#     if request.method == 'POST':
#         mobile = request.POST.get('mobile')
#         fname = request.POST.get('first_name')
#         lname = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         if password1 == password2:
#             MyUser.objects.create_user(first_name=fname, last_name=lname, email=email, username=mobile,
#                                        password=password1, user_type='3').save()
#             messages.success(request, 'You are Signup Successfully and Interesting Use Other Future Please Login')
#             return HttpResponseRedirect(reverse('login'))
#         else:
#             messages.error(request, 'Conform Password Not Match')
#             return HttpResponseRedirect(reverse('signup'))
#     else:
#         return render(request, 'logintemplates/signup.html')


