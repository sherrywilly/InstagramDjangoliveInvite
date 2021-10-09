from __future__ import absolute_import, unicode_literals

import random

from celery import shared_task, Celery
from datetime import datetime
from celery.schedules import  crontab
from django.http import JsonResponse
import time as t
from core.functions import get_shortcode_from_explore, get_time_line, comment, get_user_by_id, get_users_from_shortcode, \
    like, get_shortcode_from_reels, start
from core.models import IgUser, Status
from django.db import transaction



# @shared_task(name='comment')
# def tester():
#     x = IgUser.objects.all().first()
#     # print(x)
#     y = get_time_line(user=x)
#     count = 0
#     for m in y['items']:
#         try:
#             print("=============================================")
#             taken = m['taken_at']
#             now_timestamp = t.time()
#             difference = float(now_timestamp) - float(taken)
#             print(difference)
#             if difference < 300:
#                 print("3 min")
#                 if count < 1:
#                     media_id = m['id']
#                     l = comment(user=x, mediaId=media_id, commentText="❤")
#                     lil = like(user=x, mediaId=media_id)

#                     print(l)
#                     print(lil)
#                     count += 1
#                     break

#         except Exception as e:
#             print(e)
#             pass


#     #
#     return y

@shared_task(name='inviter')
def invite(name):
    _now = datetime.now().time()
    with transaction.atomic():
        y = IgUser.objects.filter(username=name,active=True,ftime__lte=_now, ttime__gte=_now).first()
        # y = get_user_by_id(user=x,user_id='9657000400')
        if not y:
            return {'status':"Fail",'message':"inactive"}
        x = y.desc
        #   json.loads(y.json)
        IgUser.objects.filter(username=name,active=True).update(desc="4619342150,")

        j =get_user_by_id(user=y,user_id=x)
        Status.objects.create(ig_id=y,comment=x,response=j)
    # return HttpResponse(y)
    return j
    

@shared_task(name='userlist')
def get_users():
    _now = datetime.now().time()
    users = IgUser.objects.filter(active=True,ftime__lte=_now, ttime__gte=_now)
    # y = get_user_by_id(user=x,user_id='9657000400')
    if not users:
            return {'status':"Fail",'message':"inactive"}
    for y in users:
        try:
            random_bit = random.getrandbits(1)
            random_boolean = bool(random_bit)
            if random_boolean:
                print("------------- SHORTCODE FROM REELS -------------")
                x = get_shortcode_from_reels(user=y)
            else:
                print("------------- SHORTCODE FROM EXPLORE -------------")
                x = get_shortcode_from_explore(cookie=y.cookie)
            x = x['items'][0]['media']['code']
            
            x= get_users_from_shortcode(cookie=y.get_slave,shortcode=x)
            y = IgUser.objects.get(id=y.id)
            y.desc = y.desc+",".join(x)+","
            y.save()
        except Exception as x:
            Status.objects.create(status='Fail',ig_id=y,comment=x,response="FAILED TO FETCH USERS")
            continue
    return {'status':'ok'}


@shared_task(name='live_creator')
def live_create():
    _now = datetime.now().time()
    users = IgUser.objects.filter(active=True,ftime__lte=_now, ttime__gte=_now)
    # y = get_user_by_id(user=x,user_id='9657000400')
    if not users:
            return {'status':"Fail",'message':"inactive"}
    for y in users:
        try:
            start(user=y)
        except:
            pass
    return {'status':'ok'}