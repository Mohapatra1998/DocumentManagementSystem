from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse
from LoginApp.models import Document, MyUser
from django.contrib import messages
from django.db.models import Q
# Create your views here.
def manager_dashboard(request):
    approve_doc = Document.objects.filter(aproved_by_manager = "1").count()
    pending_doc = Document.objects.filter(aproved_by_manager = "3").count()
    reject_doc = Document.objects.filter(aproved_by_manager = "2").count()
    all_doc = Document.objects.all().count()

    recent_doc = Document.objects.all().order_by('-updated_at')[:3].select_related('user')

    context={
        "approve_doc":approve_doc,
        "pending_doc":pending_doc,
        "reject_doc":reject_doc,
        "recent_doc":recent_doc,
        "all_doc":all_doc,

    }

    return render(request, 'managertemplates/managerdashboard.html',context)
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
    #     return HttpResponseRedirect(reverse('managerdashboard'))
    # else:
    #     return render(request, 'managertemplates/managerdashboard.html')


def managerlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
def view_document(request):
    document = Document.objects.all().order_by('-updated_at')
    #document = Document.objects.filter(Q(aprove_by_manager='2')|Q(aprove_by_manager='1'))
    return render(request, 'managertemplates/viewdocument.html',{"document":document})
def document_details(request,id):
    document = Document.objects.get(id = id)
    return render(request, 'managertemplates/document_details.html', {"document": document})


def approve_status(request):
    if request.method == "POST":
        document_id = request.POST.get('document_id')
        approve = request.POST.get('approve')
        document = Document.objects.get(id=document_id)
        document.aproved_by_manager=approve
        document.save()
        return HttpResponseRedirect(reverse('managerviewdocument'))
      
    else:
        return HttpResponseRedirect(reverse('managerviewdocument'))

def search_manager(request):
    if request.user.is_authenticated:
        query = request.GET['query']
        if len(query)>20 or len(query) == 0:
            document = Document.objects.none()
        else:
            document = Document.objects.filter(name__icontains=query)
        if document.count() == 0:
            messages.warning(request, 'No search results found. Please refine your query')

        return render(request, 'managertemplates/viewdocument.html', {'document':document, 'query':query})
    else:
        return HttpResponseRedirect(reverse('login'))
# def ad_search_manager(request):
#     document = Document.objects.all()
#     document_filter = DocumentFilter(request.GET, queryset=document)
#     return render(request, 'managertemplates/ad_search_manager.html', {'filter', document_filter})
def ad_search_form(request):
    return render(request, 'managertemplates/ad_search_form.html')


def ad_search_manager(request):
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

    return render(request, 'managertemplates/viewdocument.html', {'document':document})

