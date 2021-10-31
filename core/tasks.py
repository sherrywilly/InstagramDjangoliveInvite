from __future__ import absolute_import, unicode_literals

import random

from celery import shared_task, Celery
from datetime import datetime
from celery.schedules import  crontab
from django.http import JsonResponse
import time as t

import requests
from core.functions import get_shortcode_from_explore, get_time_line, comment, get_user_by_id, get_users_from_shortcode, \
    like, get_shortcode_from_reels, start, upload_photo
from core.models import IgUser, PicShedule, Status
from django.db import transaction

from core.thread import InstaGetUserThread, InstaInviteThread



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
def invite():
    _now = datetime.now().time()
    users = IgUser.objects.filter(active=True,ftime__lte=_now, ttime__gte=_now)
        # y = get_user_by_id(user=x,user_id='9657000400')
    if not users:
        return {'status':"Fail",'message':"inactive"}
    for y in users:
        InstaInviteThread(y.pk).start()
    # return HttpResponse(y)
    return {"status":"ok"}
    

@shared_task(name='userlist')
def get_users():
    _now = datetime.now().time()
    users = IgUser.objects.filter(active=True,ftime__lte=_now, ttime__gte=_now)
    # y = get_user_by_id(user=x,user_id='9657000400')
    if not users:
            return {'status':"Fail",'message':"inactive"}
    for y in users:
        InstaGetUserThread(y.pk).start()
    return {'status':'ok'}



@shared_task(name="request")
def requester(url):
    requests.get(url)
    return {"Status":"ok"}


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
import datetime
@shared_task(name="img_upload")
def pic_uploader():
    __now = datetime.datetime.now()
    range = datetime.timedelta(minutes=5)
    before_five = __now-range
    x = PicShedule.objects.filter(datetime__gte=before_five,datetime__lte=__now,is_done=False )
    print(x)
    for i in x:
        pic = str(i.image.url).lstrip('/')
        upload_photo(photo=pic,user=i.iguser,options={'rename':False},caption=i.caption)
        i.delete()
    return {"Status":"ok"}