from django.shortcuts import render, HttpResponseRedirect
from LoginApp.models import Document, MyUser
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import os,qrcode,random,io
from datetime import datetime


# Create your views here.
def user_dashboard(request):
    # if request.method == 'POST':
    #     mobile = request.POST.get('mobile')
    #     fname = request.POST.get('first_name')
    #     lname = request.POST.get('last_name')
    #     email = request.POST.get('email')
    #     myuser = MyUser.objects.get(id=request.user.id)
    #     myuser.first_name = fname
    #     myuser.last_name = lname
    #     myuser.email = email
    #     myuser.username = mobile
    #     myuser.save()
    #     messages.success(request, 'Data Updated Successfully')
    #     return HttpResponseRedirect(reverse('userdashboard'))
    
    approve_doc = Document.objects.filter(aproved_by_admin = "1",user = request.user.id).count()
    pending_doc = Document.objects.filter(aproved_by_admin = "3",user = request.user.id).count()
    reject_doc = Document.objects.filter(aproved_by_admin = "2",user = request.user.id).count()

    recent_doc = Document.objects.filter(user = request.user.id).order_by('-updated_at')[:3].select_related('user')

    context={
        "approve_doc":approve_doc,
        "pending_doc":pending_doc,
        "reject_doc":reject_doc,
        "recent_doc":recent_doc
    }

    return render(request, 'usertemplates/userdashboard.html',context)


def document_upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            file = request.FILES.get('file')
            description = request.POST.get('description')
            file_type = request.POST.get('file_type')
            file_numble = request.POST.get('file_numble')
            department = request.POST.get('department')
            review = request.POST.get('review')
            user = request.user
            if user.user_type != '1' or user.user_type != '2':
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@upload document @@@@@@@@@@@@2@@')
                doc = Document(user=MyUser.objects.get(id=request.user.id), name=name, file=file,
                         description=description, file_type=file_type, file_numble=file_numble, department=department,
                         review=review)
                doc.save()
                link = "http://127.0.0.1:8000/document/drawnig/no/" + str(doc.id)
                img = qrcode.make(link)
                qr_name = "static/Qr_img/"+"Qr"+str(random.randint(100000000000,999999999999))+'.PNG'
                img.save(qr_name)
                doc.qr_code = qr_name
                doc.save()
                messages.success(request, 'Document Upload Successfully')
                return HttpResponseRedirect(reverse('viewdocument'))
            else:
                messages.error(request, 'Document Upload Fail')
                return HttpResponseRedirect(reverse('uploaddocument'))
        else:
            return render(request, 'usertemplates/docuploadform.html')
    else:
        return HttpResponseRedirect(reverse('login'))


def view_document(request):
    document = Document.objects.filter(user=request.user.id).order_by('-updated_at')
    return render(request, 'usertemplates/viewdocument.html', {"document": document})
def document_details(request,id):
    document = Document.objects.get(id = id,user = request.user.id)
    return render(request, 'usertemplates/document_details.html', {"document": document})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def search_user(request):
    if request.user.is_authenticated:
        query = request.GET['query']
        if len(query) > 20 or len(query) == 0:
            document = Document.objects.none()
        else:
            document = Document.objects.filter(name__icontains=query, user=request.user.id)
        if document.count() == 0:
            messages.warning(request, 'No search results found. Please refine your query')

        return render(request, 'usertemplates/viewdocument.html', {"document": document})
    else:
        return HttpResponseRedirect(reverse('login'))


def update_document(request, id):
    upd_doc= Document.objects.get(id = id)
    if upd_doc.aproved_by_manager != "1":
        if request.method == 'POST':
            pi = Document.objects.get(id=id)
            pi.name = request.POST.get('name')
            pi.description = request.POST.get('description')
            pi.department = request.POST.get('department')
            pi.file_type = request.POST.get('file_type')
            pi.file_numble = request.POST.get('file_numble')
            pi.review = request.POST.get('review')
            # pi.file = request.FILES.get('file')
            # if pi.qr_code != None:
            #      old_qr = pi.qr_code
            #      os.remove(str(old_qr))
        
            link = "http://127.0.0.1:8000/document/drawnig/no/"+str(pi.id)
            img = qrcode.make(link)
            qr_name = "static/Qr_img/"+"Qr"+str(random.randint(100000000000,999999999999))+'.PNG'
            img.save(qr_name)
            pi.qr_code = qr_name
            pi.updated_at = datetime.now()

            # if request.FILES.get('file') != None:
            #     old_file = pi.file
            #     os.remove(os.path.join('media', str(old_file)))
            #     pi.file = request.FILES.get('file')
            pi.save()
            messages.success(request, 'Data Updated Successfully')
            return HttpResponseRedirect(reverse('document_details' ,kwargs={"id":pi.id}))
        else:
            pi = Document.objects.get(id=id)
            return render(request, 'usertemplates/update.html',{'pi': pi})
    else:
        return HttpResponseRedirect(reverse('viewdocument'))






def ad_search_form2(request):
    return render(request, 'usertemplates/ad_search_form2.html')

def ad_search_user(request):
    filename = request.GET['filename']
    filenumble = request.GET['filenumble']
    file_type = request.GET['file_type']
    


    department = request.GET['department']

    if len(filename)>20 or len(filename) == 0:
        document = Document.objects.none()
    else:
        document = Document.objects.filter(name__icontains=filename, file_type=file_type, file_numble=filenumble, department=department)
    if document.count() == 0:
        messages.warning(request, 'No search results found. Please refine your query')

    return render(request, 'usertemplates/viewdocument.html', {'document':document})