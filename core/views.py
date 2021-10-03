from django.http import response
from django.http.response import JsonResponse
# from core.decorators import session_not_exist
import json
from core.functions import *
from core.models import *
from core.forms import *
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

# Create your views here.
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

            else:

                print(username+" "+password)
                x = Mylogin(username, password)
                y = json.loads(x.text)
                if y['status'] == 'ok':
                    IgUser.objects.create(username=username, password=password, cookie=x.cookies.get_dict(
                    ), pro_pic=y['logged_in_user']['profile_pic_url'])
                    request.session['username'] = username
                    return redirect('dash/')
                else:
                    msg = y['message']

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



    context = {
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
    return  JsonResponse(y)

def tester(request):
    y = IgUser.objects.all().last()
    start(user=y)
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
    #
    # j = get_user_by_id(user=y, user_id=x)

    return JsonResponse({'status':"ok"})