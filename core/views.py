from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from core.decorators import session_not_exist
from core.forms import *
from core.functions import *
from core.models import *
from core.thread import InstaGetUserThread, InstaInviteThread


# from core.decorators import session_not_exist
# Create your views here.


@csrf_exempt
def LoginView(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            try:
                u = IgUser.objects.get(username__iexact=username)
            except:
                u = None
            if not u is None:
                # user = IgUser.objects.get(username__iexact=username)
                x = Mylogin(username, password)
                y = json.loads(x.text)
                # print(y)
                if y['status'] == 'ok':
                    u.password = password
                    u.pro_pic = y['logged_in_user']['profile_pic_url']
                    u.cookie = x.cookies.get_dict()
                    u.save()
                    request.session['username'] = username
                    return redirect('dash/')
                else:
                    msg = y['message']
                    return JsonResponse({'status': 'Fail', 'message': msg})

            else:

                print(username + " " + password)
                x = Mylogin(username, password)
                y = json.loads(x.text)
                if y['status'] == 'ok':
                    IgUser.objects.create(username=username, password=password, cookie=x.cookies.get_dict(
                    ), pro_pic=y['logged_in_user']['profile_pic_url'])
                    request.session['username'] = username
                    return redirect('dash/')
                else:
                    msg = y['message']
                    JsonResponse({
                        'message': msg,
                        "status": "Fail"
                    })

            # return HttpResponse("text")
    context = {
        'form': form,
        'msg': msg
    }
    return render(request, "accounts/login.html", context)


def dashboard(request):
    try:
        user = IgUser.objects.get(username=request.session['username'])
    except:
        del request.session['username']
        return redirect('/')

    form = IgUpdateForm(user, request.POST or None, instance=user)
    print(form)
    if request.method == "POST":
        if form.is_valid():
            form.save()
        else:
            pass
    context = {
        'form': form,
        'title': "User Settings to run",
        'user': user,
        'btn': "update"
    }
    return render(request, "form.html", context)


def tester1(request):
    x = IgUser.objects.all().first()
    # print(x)
    y = get_time_line(user=x)
    count = 0
    for m in y['items']:
        try:
            print("=============================================")
            taken = m['taken_at']
            now_timestamp = t.time()
            difference = float(now_timestamp) - float(taken)
            print(difference)
            if difference < 30000:
                print("3 min")
                if count < 1:
                    media_id = m['id']
                    l = comment(user=x, mediaId=media_id, commentText="❤")
                    lil = like(user=x, mediaId=media_id)

                    print(l)
                    print(lil)
                    count += 1
                    break

        except Exception as e:
            print(e)
            pass

    #
    return JsonResponse(y)


def tester(request, user):
    try:
        y = IgUser.objects.get(username__iexact=user)
    except:
        return JsonResponse({'status': "Fail"})
    print(y)
    try:
        start(user=y)
    except Exception as e:
        return JsonResponse({'status': "Fail", "message": e})

    # y = get_user_by_id(user=x,user_id='9657000400')
    # x = get_shortcode_from_explore(cookie=y.get_slave)
    # x = x['items'][0]['media']['code']
    # x= get_users_from_shortcode(cookie=y.get_slave,shortcode=x)
    # #   json.loads(y.json)
    # x = ",".join(x)+",9657000400"

    # j =get_user_by_id(user=y,user_id=x)
    # print(j)
    # return HttpResponse(y)
    # y = IgUser.objects.all().first()
    # # y = get_user_by_id(user=x,user_id='9657000400')
    # x = get_shortcode_from_explore(cookie=y.get_slave)
    # x = x['items'][0]['media']['code']
    # x = get_users_from_shortcode(cookie=y.get_slave, shortcode=x)
    # #   json.loads(y.json)
    # x = ",".join(x) + ",9657000400"
    # print(x)
    # j = get_user_by_id(user=y, user_id=x)

    return JsonResponse({'status': "ok"})


# sherry1Jerry


@session_not_exist
def status_view(request):
    try:
        user = IgUser.objects.get(username=request.session['username'])
    except:
        del request.session['username']
        return redirect('/')
    try:
        data = user.status_set.all()[:10]
    except:
        data = Status.objects.all()[:10]
    context = {
        'reports': data,
        'user': user
    }
    return render(request, "status.html", context)


def logout_view(request):
    try:
        del request.session['username']
    except:
        pass

    return redirect('/')


@session_not_exist
def addSlave(request):
    if 'username' not in request.session:
        user = None
    else:
        try:
            user = IgUser.objects.get(username=request.session['username'])
        except:
            del request.session['username']
            return redirect('/')

    form = SlaveForm(request.POST or None)
    slave = SlaveUser.objects.filter(created_by=user.username)
    print(slave)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            u = form.save(commit=False)
            x = Mylogin(username, password)
            y = json.loads(x.text)
            if y['status'] == 'ok':

                u.cookie = x.cookies.get_dict()
                try:

                    pic = y['logged_in_user']['profile_pic_url']
                except:
                    pic = None

                u.pro_pic = pic
                u.created_by = user.username
                u.save()
                messages.success(
                    request, "successfully loged in your slave account")
                return HttpResponseRedirect(reverse('addslave'))
            else:
                messages.error(request, y['message'])
                return HttpResponseRedirect(reverse('addslave'))
        else:
            # messages.error(request, form.errors)
            print(form.errors)

    context = {
        'form': form,
        'slave': slave,
        'user': user,
        'title': "add slave account",
        'btn': "login"
    }
    return render(request, "slave/form.html", context)


@session_not_exist
def deleteSlave(request, pk):
    if request.method == "POST":
        SlaveUser.objects.get(id=pk).delete()
        return redirect(reverse('addslave'))
    else:
        HttpResponse("You are not authorized to make this request")


def UserManage(request, pk):
    if 'username' not in request.session:
        user = None
    else:
        try:
            user = IgUser.objects.get(username=request.session['username'])
        except:
            del request.session['username']
            return redirect('/')
    if request.method == "POST":
        if user.verified:
            user.active = not user.active
            user.save()
            return redirect(reverse('dash'))
        else:
            return HttpResponse("please contact the provider to access this feature")
    else:
        return HttpResponse(" you are not allowed to process this request")


def get_users():
    _now = datetime.now().time()
    users = IgUser.objects.filter(
        active=True, ftime__lte=_now, ttime__gte=_now)
    # users = IgUser.objects.all()
    return users


def fetch_users(request):
    users = get_users()
    if not users.exists():
        return JsonResponse({"status": "ok", "message": "No users available"})
    key = request.GET.get('key')
    if key == "mom":
        for i in users:
            # print(i.pk)
            # x = i.pk
            InstaGetUserThread(i.pk).start()
            # time.sleep(5)
    else:
        return JsonResponse({"status": "Fail"})

    return JsonResponse({"status": "ok"})


def insta_invite(request):
    users = get_users()
    if not users.exists():
        return JsonResponse({"status": "ok", "message": "No users available"})
    key = request.GET.get('key')
    if key == "mom":
        for y in users:
            print("-------------INVITE -------------")
            InstaInviteThread(y.pk).start()
            # try:
            #     x = y.desc
            #     #   json.loads(y.json)
            #     IgUser.objects.filter(username=y.username,active=True).update(desc="4619342150,")
            #     j =get_user_by_id(user=y,user_id=x)
            #     Status.objects.create(ig_id=y,comment=x,response=j)
            # except Exception as e:
            #     print("----",e)
            #     Status.objects.create(ig_id=y,comment="SOME THING WENT WRONG IN INVITE",response=e,status="Fail")
    else:
        return JsonResponse({"status": "Fail"})

    return JsonResponse({"status": "ok"})


def tester1(request):
    users =IgUser.objects.all()
    
    for i in users:
        # print(i.username)
        mids = []
        short_codes = [x["media"]["code"] for x in get_shortcode_from_reels(i)['items']]
        for shortcode in short_codes:
            # print(shortcode)
            users = get_users_from_shortcode(cookie=i.cookie, shortcode=shortcode,proxy=i.proxy)
            media_ids = get_story_by_user_ids(user=i, user_ids=users)
            # for media in media_ids:
                # print(media)
                # print("-----------------")
            mids.extend(media_ids)
        send_story_like(i, mids)
            # for user in users:
            # print(user)
            # try:
            #     media_ids =get_last_highlights(i, user)
            #     for media_id in media_ids:
            #         print(media_id)
            #         send_story_like(i, media_id)
            # except Exception as e:
            #     print(e)
            #     continue

    return JsonResponse({"status": "ok"})
