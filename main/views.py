from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import profile_user
from .models import create_projects, msgs, img_create, realtors, front_end, back_end, basics, project_details, project_sample, aboutus, contacts, contact_s
from django.core.paginator import Paginator
def index(request):
    if request.user.is_authenticated:
        prof = profile_user.objects.get(user_id=request.user.id)
    else:
        prof = None
    basic = basics.objects.all()
    realtor = realtors.objects.all()
    front = front_end.objects.all()
    back = back_end.objects.all()
    projects = project_sample.objects.all()[:6]
    context = {'basic': basic, 'realtor': realtor, 'front': front, 'back': back, 'projects': projects, 'prof': prof}
    return render(request,'index.html', context=context)

def create_project(request):
    img = img_create.objects.all()
    if request.user.is_authenticated:
        prof = profile_user.objects.get(user_id=request.user.id)

        if request.method == 'POST':
            description = request.POST['description']
            project_name = request.POST['project_name']
            project_description = request.POST['project_description']
            langu = request.POST['langu']
            price = request.POST['price']
            day = request.POST['day']
            create_proj = create_projects(
                project_name=project_name,
                description=description,
                project_description=project_description,
                user=request.user,
                langu=langu,
                price=price,
                day=day
            )
            create_proj.save()
            messages.success(request, 'پروژه شما ایجاد شد شما الان میتوانید در پروفایلتان ان را مشاهده کنید و با باز کردن ان پیام ها را ادامه دهید')
            return redirect('create_project')
        return render(request, 'create-project.html', {'prof': prof, 'img': img})
    else:
        messages.success(request, 'برای ایجاد پروژه مورد نظرتان ابتدا وارد سایت شوید')
        return redirect('login_user')

def confirms_project(request, pk):
    if request.user.is_authenticated:
        prof = profile_user.objects.get(user_id=request.user.id)
    else:
        prof = None
    creative = create_projects.objects.get(id=pk)
    massage = msgs.objects.filter(confirm_pro=creative.id)
    user_name = request.user
    mass = msgs.objects.filter(confirm_pro=creative.id).exclude(user=user_name)

    unread_messages = msgs.objects.filter(confirm_pro=creative.id, is_read=False).exclude(user=user_name)
    if unread_messages.exists():
        unread_messages.update(is_read=True, read_date1=datetime.now(), read_date2=datetime.now())
    data = []
    for msg in massage:
        dating_1 = msg.date_1
        dating_2 = msg.date_3
        data.append({
            'date_persian': dating_1,
            'date_america': dating_2
        })
    if request.method == 'POST':
        description = request.POST['description']
        description_2 = request.POST['description_2']
        confirm_pro = request.POST['confirm_pro']
        reply = request.POST['reply']

        msg = msgs(
            user=request.user,
            description=description,
            confirm_msg=description_2,
            confirm_pro=confirm_pro,
            reply=reply,

        )
        msg.save()

        return redirect('confirm_project', pk)


    return render(request,'confirm-project.html' ,{'creative':creative, 'massage':massage, 'data':data, 'prof':prof})

def admins(request):
    if request.user.is_authenticated:
        prof = profile_user.objects.get(user_id=request.user.id)
    else:
        prof = None
    creatives = create_projects.objects.all()
    mass = msgs.objects.filter(is_read=False).exclude(user=request.user)

    data = []
    for creative in creatives:
        unread_count = msgs.objects.filter(confirm_pro=creative.id, is_read=False).exclude(user=request.user)
        data.append({
            'creative':creative,
            'unread_count':unread_count.count()
        })
    print(data)
    context = {'creatives':creatives, 'mass':mass, 'data':data, 'prof':prof}
    return render(request, 'admin.html', context=context)

def details_project(request, pk):
    if request.user.is_authenticated:
        prof = profile_user.objects.get(user_id=request.user.id)
    else:
        prof = None
    projects = project_sample.objects.get(id=pk)
    projects_details =project_details.objects.filter(for_project_id=pk)
    context = {'projects':projects, 'projects_details':projects_details, 'prof':prof}
    return render(request, 'details.project.html', context=context)


def about(request):
    if request.user.is_authenticated:
        prof = profile_user.objects.get(user_id=request.user.id)
    else:
        prof = None
    abouting = aboutus.objects.all()
    realtor = realtors.objects.all()
    context = {'realtor':realtor, 'abouting':abouting, 'prof':prof}
    return render(request, 'profile.html', context=context)

def all_projects(request):
    if request.user.is_authenticated:
        prof = profile_user.objects.get(user_id=request.user.id)
    else:
        prof = None
    projects = project_sample.objects.all()
    paginator = Paginator(projects, 6)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {'projects':page_obj, 'prof':prof}
    return render(request, 'more-portfolio.html', context=context)

def contact(request):
    if request.user.is_authenticated:
        prof = profile_user.objects.get(user_id=request.user.id)
    else:
        prof = None
    contacting = contacts.objects.all()
    realtor = realtors.objects.all()
    context = {'realtor': realtor, 'contacting':contacting, 'prof':prof}
    return render(request, 'contact.html', context=context)

def deleted_message(request, pk, id):

    msg = msgs.objects.get(id=pk)
    msg.delete()
    return redirect('confirm_project', id)

def contact_site(request):
    uri = request.path
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        email = request.POST['email']
        url = request.POST['url']
        print(url)
        cont = contact_s(
            name=name,
            contact=contact,
            email=email,
        )
        cont.save()
        messages.success(request, 'نظر شما با موفقیت ثبت شد. ممنون از ثبت نظر شما')
        return redirect(url)
    return redirect(uri)
