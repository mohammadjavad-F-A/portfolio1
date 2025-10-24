from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import profile_user, users_pass
from django.contrib import messages
from main.models import create_projects, msgs
from django.core.mail import send_mail
from django.conf import settings
def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید')
            return redirect('profile')
        else:
            messages.error(request, 'رمز ورود یا نام کاربری اشتباه است')
            return redirect('login_user')
    return render(request, 'login.html')

def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        last_name = request.POST['family']
        username = request.POST['username']
        email = request.POST['email']

        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(email=email).exists():
            messages.error(request, 'این ایمیل از قبل وجود دارد')
            return redirect('sign_up')
        if User.objects.filter(username=username).exists():
            messages.success(request, 'نام کاربری از قبل وجود دارد وارد شوید')
            return redirect('login_user')
        if password1 != password2:
            messages.error(request, "رمز عبور با هم همخوانی ندارد")
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password2
            )
            user.save()
            prof = profile_user(
                user_name=username,
                user_id=user.id,
            )
            prof.save()
            passwords = users_pass(
                user=username,
                userid=user.id,
                password=password2,
                email=email,
            )
            passwords.save()

            send_mail(
                "کارفرمای عزیز" + '' + username,
                "به سایت کارفرما شو خوش امدید شما میتوانید در اینجا به کارفرما تبدیل شوید و پروژه های خودتان را بدون هیچ دردسری ایجاد کنید",
                settings.EMAIL_HOST_USER,
                [user.email, "m79516287@gmail.com"],
                fail_silently=True
            )
            messages.success(request, 'ثبت نام شما در سایت تکمیل شد وارد شوید')
            return redirect('login_user')

    return render(request, 'signup.html')

def profile(request):
    if request.user.is_authenticated:
        proj = create_projects.objects.filter(user=request.user)
        user = User.objects.get(id=request.user.id)
        prof = profile_user.objects.get(user_id=request.user.id)
        pass_user = users_pass.objects.get(userid=request.user.id)
        data = []
        for pro in proj:
            unread_count = msgs.objects.filter(confirm_pro=pro.id, is_read=False).exclude(user=request.user)
            data.append({
                'pro': pro,
                'unread_count': unread_count.count()
            })


        if request.method == 'POST':
            name = request.POST['name']
            family = request.POST['family']
            username = request.POST['username']
            email = request.POST['email']
            user.first_name = name
            user.last_name = family
            user.username = username
            user.email = email
            user.save()
            prof.user_name=username
            prof.save()
            pass_user.user = username
            pass_user.email = email
            pass_user.save()
            messages.success(request, 'اطلاعات کاربری با موفقیت تغییر یافت')
            return render(request, 'user-profile.html', {'user': user, 'prof': prof, 'proj': proj, 'data': data})
        context = {'user': user, 'prof': prof, 'proj': proj, 'data': data}
        return render(request,'user-profile.html', context=context)
    else:
        messages.success(request, 'کاربر گرامی برای مشاهده پروفایل ثبت نام و وارد سایت شوید')
        return redirect('login_user')


def logout_user(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید')
    return redirect('index')

def prof_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        user_id = request.POST['user_id']
        img = request.FILES['img']
        user_prof = profile_user.objects.get(user_id=user_id)
        user_prof.img = img
        user_prof.save()
        messages.success(request, 'پروفایل با موفقیت ذخیره شد')
        return redirect('profile')
    return render(request, 'user-profile.html')

def forgot_pass(request):

    if request.method == 'POST':
        email = request.POST['email']

        pass_user = users_pass.objects.get(email=email)
        if pass_user:
            password = pass_user.password
            user = pass_user.user

            send_mail(
                 'کاربر عزیز',
                'کاربر' + '' + user + '' + 'به خدمت شما میرساند رمز شما در سایت کارفرما شو' + '' + password + '' + 'است',
                settings.EMAIL_HOST_USER,
                [pass_user.email, "m79516287@gmail.com"],
                fail_silently=True

            )
            messages.success(request, 'پسورد به ایمیل شما پیامک شد')
            return redirect('login_user')
        else:
            messages.error(request, 'کاربری با این ایمیل یافت نشد')
            return redirect('forgot_pass')
    return render(request, 'forgot.html')
def change_password(request):
    if request.user.is_authenticated:
        prof = profile_user.objects.get(user_id=request.user.id)
    else:
        prof = None
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = request.user
        if user.email != email:
            messages.error(request, 'ایمیل فعلی نادرست است')
            return redirect('change_password')
        if not user.check_password(password):
            messages.error(request, 'رمز فعلی شما نادرست است')
            return redirect('change_password')
        if new_password != confirm_password:
            messages.error(request, 'رمز جدید یا تکرار ان نادرست است')
            return redirect('change_password')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        pass1 = users_pass.objects.get(email=email)
        pass1.password = new_password
        pass1.save()
        send_mail(
            'تغییر رمز',
            'رمز شما در سایت تغییر کرد لطفا آن را در اختیار دیگران قرار ندهید',
            settings.EMAIL_HOST_USER,
            [user.email, "m79516287@gmail.com"],
            fail_silently=True
        )
        messages.success(request, 'رمز شما با موفقیت تغییر کرد')
        return redirect('profile')
    return render(request, 'change-password.html', {'prof': prof})


