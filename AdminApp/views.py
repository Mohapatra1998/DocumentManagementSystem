#from typing_extensions import ParamSpec
from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect
from LoginApp.models import MyUser, Document, Admin
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime


# Create your views here.


# Create your views here.
#def admin_dashboard(request):
    
    # if request.method == 'POST':
    #     mobile = request.POST.get('mobile')
    #     fname = request.POST.get('first_name')
    #     lname = request.POST.get('last_name')
    #     email = request.POST.get('email')
    #     myuser = MyUser.objects.get(id = request.user.id)
    #     myuser.first_name=fname
    #     myuser.last_name=lname
    #     myuser.email=email
    #     myuser.username=mobile
    #     myuser.save()
    #     messages.success(request, 'Data Updated Successfully')
    #     return HttpResponseRedirect(reverse('admindashboard'))

   # else:
        # return render(request, 'admintemplates/admindashboard.html')



def admin_dashboard(request):
    approve_doc = Document.objects.filter(aproved_by_manager = "1").count()
    pending_doc = Document.objects.filter(aproved_by_manager = "3").count()
    reject_doc = Document.objects.filter(aproved_by_manager = "2").count()
    all_doc = Document.objects.all().count()

    #recent_doc = Document.objects.filter(aprove_by_manager='1').order_by('-updated_at')[:3].select_related('user')

    context={
        "approve_doc":approve_doc,
        "pending_doc":pending_doc,
        "reject_doc":reject_doc,
        "all_doc":all_doc,

    }

    return render(request, 'admintemplates/admindashboard.html',context)



def view_user(request):
    user = MyUser.objects.filter(user_type='3')
    return render(request, 'admintemplates/viewuser.html', {"user": user})


def view_manager(request):
    user = MyUser.objects.filter(user_type='2')
    return render(request, 'admintemplates/viewmanager.html', {"user": user})


def add_manager(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            MyUser.objects.create_user(first_name=fname, last_name=lname, email=email, username=mobile,
                                       password=password1, user_type='2').save()
            messages.success(request, 'Add Manager Successfully')                            
            return HttpResponseRedirect(reverse('viewmanager'))
        else:
            messages.error(request, 'Conform Password not match')
            return HttpResponseRedirect(reverse('addmanager'))
    else:
        return render(request, 'admintemplates/addmanager.html')


def adminlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def view_document(request):
    document = Document.objects.filter(aproved_by_manager='1').order_by('-updated_at')
    return render(request, 'admintemplates/viewdocument.html', {"document": document})

def document_details(request,id):
    document = Document.objects.get(id = id, aproved_by_manager='1')
    return render(request, 'admintemplates/document_details.html', {"document": document})



def approve_status(request):
    if request.method == "POST":
        document_id = request.POST.get('document_id')
        approve = request.POST.get('approve')
        reject_reason = request.POST.get('reject_reason')
        document = Document.objects.get(id=document_id)
        document.aproved_by_admin = approve
        document.reject_reason = reject_reason
        document.save()
        return HttpResponseRedirect(reverse('adminviewdocument'))
    else:
        return HttpResponseRedirect(reverse('adminviewdocument'))


def search_admin(request):
    if request.user.is_authenticated:
        query = request.GET['query']
        if len(query) > 20 or len(query) == 0:
            document = Document.objects.none()
        else:
            document = Document.objects.filter(name__icontains=query, aproved_by_manager='1')
        if document.count() == 0:
            messages.warning(request, 'No search results found. Please refine your query')

        #return render(request, 'admintemplates/adminsearch.html', {'document': document, 'query': query})
        return render(request, 'admintemplates/viewdocument.html', {"document": document, 'query':query})
    else:
        return HttpResponseRedirect(reverse('login'))







def add_user(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            MyUser.objects.create_user(first_name=fname, last_name=lname, email=email, username=mobile,
                                       password=password1, user_type='3').save()
            messages.success(request, 'Add User Successfully')
            return HttpResponseRedirect(reverse('viewuser'))
        else:
            messages.error(request, 'Conform Password Not Match')
            return HttpResponseRedirect(reverse('adduser'))
    else:
        return render(request, 'admintemplates/adduser.html')



def ad_search_form1(request):
    return render(request, 'admintemplates/ad_search_form1.html')


def ad_search_admin(request):

    filename = request.GET['filename']
    filenumble = request.GET['filenumble']
    file_type = request.GET['file_type']
    department = request.GET['department']

    if len(filename)>20 or len(filename) == 0:
        document = Document.objects.none()
    else:
        document = Document.objects.filter(name__icontains=filename, file_type=file_type, file_numble=filenumble, department=department, aproved_by_manager='1')
    if document.count() == 0:
        messages.warning(request, 'No search results found. Please refine your query')

    return render(request, 'admintemplates/viewdocument.html', {"document": document})


  