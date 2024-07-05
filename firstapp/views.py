from django.shortcuts import render,redirect
from .forms import Index_form,Signup,Fg_username,Fg_confirm
from .models import Message,Activity
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
def index(request):
    form = Index_form()
    if request.method == 'POST':
        form = Index_form(request.POST)
        if form.is_valid():
            create_grp = form.cleaned_data['create_group']
            search_grp = form.cleaned_data['search_group']
            status = form.cleaned_data['status']
            request.session['create_group'] = create_grp
            request.session['search_group'] = search_grp
            request.session['status'] = status
            return redirect("/chat_view")
    msg = Message.objects.filter(username=request.user, admin=True)
    request_dict = {}
    if len(msg)>0:
        request_obj = []
        for m in msg:
            if len(m.request_grp) > 0:
                request_obj.append(m)
        if len(request_obj) > 0:
            for obj in request_obj:
                list1 = obj.request_grp.split(",")
                request_dict[obj] = list1[0:(len(list1) - 1)]
    value = False
    if len(request_dict) > 0:
        value = True
    msg_all = Message.objects.all()
    message = []
    for i in msg_all:
        if len(i.request_grp) > 0:
            list3 = i.request_grp.split(",")
            if str(request.user) in list3:
                message.append(f"{i.room_name} is Private, Your request to join {i.room_name} has been sent to the admin,wait untill he accepts it or log in again")
    user = request.user
    return render(request,'firstapp/index.html',{'form':form,"message":message,"request_dict":request_dict,"value":value,"user":user})


create = ""
search = ""
status_grp = ""
def chat_view(request):
    create = request.session['create_group']
    search = request.session['search_group']
    status_grp = request.session['status']
    admin_info = False
    if len(search) > 0:
        admin = Message.objects.filter(room_name=search,username=request.user,admin=True)
        if len(admin) >0:
            admin_info = True
    msg = Message.objects.all()
    if create:
        act = Activity.objects.filter(room_name=search, username=request.user)
        for nt in act:
            nt.notification = 0
            nt.save()
        msg_grp = f'Admin : {request.user}'
        req = ''
        Message.objects.create(room_name=create, username=request.user, message=msg_grp, admin=True, status=status_grp,
                               request_grp=req)
        room_name = create
        username = request.user
        status = status_grp
        return render(request, 'firstapp/chat_html.html',{'room_name':room_name,'username':username,'status':status})
    elif search:
        private = False
        public = False
        for m in msg:
            if search == m.room_name:
                if m.status == "Private":
                    private = True
                elif m.status == "Public":
                    public = True
        if private:
            value = False
            for m in msg:
                if str(request.user) == str(m.username) and str(search) == str(m.room_name) :
                    value = True
                    break
            if value:
                act = Activity.objects.filter(room_name=search, username=request.user)
                for nt in act:
                    nt.notification = 0
                    nt.save()
                msg_grp = 'Hii'
                req = ''
                Message.objects.create(room_name=search, username=request.user, message=msg_grp, admin=admin_info,
                                       status=status_grp,
                                       request_grp=req)
                room_name = search
                username = request.user
                status = status_grp
                return render(request, 'firstapp/chat_html.html',
                              {'room_name': room_name, 'username': username, 'status': status})
            else:
                msg1 = Message.objects.filter(room_name=search,admin=True)

                for i in msg1:
                    list1 = i.request_grp.split(",")
                    if not str(request.user) in list1:
                        i.request_grp += str(request.user) + ","
                        i.save()
                        break
                return redirect('/index')
        elif public:
            act = Activity.objects.filter(room_name=search, username=request.user)
            for nt in act:
                nt.notification = 0
                nt.save()
            msg_grp = 'Hii'
            req = ''
            Message.objects.create(room_name=search, username=request.user, message=msg_grp, admin=admin_info,
                                   status=status_grp,
                                   request_grp=req)
            room_name = search
            username = request.user
            status = status_grp
            return render(request, 'firstapp/chat_html.html',
                              {'room_name': room_name, 'username': username, 'status': status})

def request_msg(request,name=None,room=None):
    msg = Message.objects.filter(room_name=room,username=request.user,admin=True)
    for m in msg:
        msg_grp = f"Thanks {request.user}"
        req = ""
        Message.objects.create(room_name=m.room_name, username=name, message=msg_grp, admin=False, status=m.status,
                               request_grp=req)
        break
    request_obj = []
    for m in msg:
        if m.request_grp:
            request_obj.append(m)
    for i in request_obj:
        list1 = []
        l = i.request_grp.split(",")
        for n in l:
            if name != n and n != ",":
                list1.append(n)
        str1 = ",".join(list1)
        i.request_grp = str1
        i.save()
    return JsonResponse({'status':'success'})

def auth(request):
    return render(request,'firstapp/auth.html')

def signup(request):
    form = Signup()
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('/auth')
    return render(request,'firstapp/signup.html',{'form':form})

def fg_username(request):
    form = Fg_username()
    if request.method == 'POST':
        form = Fg_username(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            request.session['username'] = user
            return redirect('/fgc')
    return render(request,'firstapp/fg_username.html',{'form':form})

user_name = ""
def fg_confirm(request):
    user_name = request.session['username']
    form = Fg_confirm()
    if request.method == 'POST':
        form = Fg_confirm(request.POST)
        if form.is_valid():
            new = form.cleaned_data['new_password']
            confirm = form.cleaned_data['confirm_password']
            if str(new) == str(confirm):
                user = get_object_or_404(User, username=user_name)
                user.set_password(confirm)
                user.save()
                return redirect('/accounts/login')
    return render(request,'firstapp/fg_confirm.html',{"form":form})

def grps_with_users(current_user):
    msg2 = Message.objects.all()
    l = []
    for grp in msg2:
        l.append(grp.room_name)
    groups = list(set(l))
    dict_grps = {}
    for i in groups:
        list2 = Message.objects.filter(room_name=i)
        user_exist = Message.objects.filter(room_name=i,username=current_user)
        users = []
        hii_users = []
        if len(user_exist) > 0:
            for objs in list2:
                if str(objs.message) == "Hii" and str(objs.username) != str(current_user) :
                    hii_users.append(objs.username)
                else:
                    users.append(objs.username)
            dict_grps[i] = users
    return dict_grps

def notification(request):
    Activity.objects.all().delete()
    current_user = request.user
    dict_grp = grps_with_users(current_user)
    dict_ref = {}
    for j in dict_grp:
        l1 = dict_grp[j][-1::-1]
        l2 = []
        for us in l1:
            if str(us) == str(request.user):
                break
            l2.append(us)
        list3 = l2[-1::-1]
        dict_ref[j] = len(list3)
    act1 = Activity.objects.filter(username=request.user)
    user_grps = Activity.objects.filter(username=request.user)
    sum_notify = 0
    for nt in dict_ref:
        sum_notify = sum_notify + dict_ref[nt]
    for n in dict_ref:
        if int(dict_ref[n]) != 0:
            Activity.objects.create(room_name=n, username=request.user, stage=False, notification=int(dict_ref[n]))
        else:
            Activity.objects.create(room_name=n, username=request.user, stage=True, notification=int(dict_ref[n]))
    act2 = Activity.objects.filter(username=request.user)
    act2_list = list(act2.values('room_name', 'notification'))
    data = {
        "status":"success",
        "act2":act2_list,
        'sum':sum_notify
    }
    return JsonResponse(data)








