import threading

from django.db import transaction
from core.functions import get_shortcode_from_explore, get_shortcode_from_reels_2, get_user_by_id, get_users_from_shortcode

from core.models import IgUser, ShortCode, Status
import random
class InstaGetUserThread(threading.Thread):
    def __init__(self, user_id):
        self.user_id = user_id
        print("______init______")
        threading.Thread.__init__(self)

    def run(self):
        print(
        " thread is running"
        )
        y = IgUser.objects.get(id=self.user_id)
        print("------------------------------------")
            
        try:
            x= get_users_from_shortcode(cookie=y.get_slave,shortcode=y.get_shortcode.code)
            y = IgUser.objects.get(id=y.id)
            y.desc = y.desc+",".join(x)+","
            y.save()
            y.get_shortcode.delete()
        except Exception as x:
            Status.objects.create(status='Fail',ig_id=y,comment=x,response="FAILED TO FETCH USERS")


class InstaInviteThread(threading.Thread):
    def __init__(self, user_id):
        self.user_id = user_id
        print("______init______")
        threading.Thread.__init__(self)

    def run(self):
        print(
        " thread is running"
        )
        y = IgUser.objects.get(id=self.user_id)
        print("----------------INVITE--------------------")
        try:

            x = y.desc
                #   json.loads(y.json)
            IgUser.objects.filter(username=y.username,active=True).update(desc="4619342150,")

            j =get_user_by_id(user=y,user_id=x)
            Status.objects.create(ig_id=y,comment=x,response=j)
        except Exception as e:
            Status.objects.create(ig_id=y,comment="SOME THING WENT WRONG IN INVITE",response=e,status="Fail")


class GetShortCodeThread(threading.Thread):
    def __init__(self,user_id):
        self.user_id = user_id
        threading.Thread.__init__(self)

    def run(self):
        print("getting shortcodes")
        y = IgUser.objects.get(id=self.user_id)
        try:
            x= get_shortcode_from_explore(cookie=y.get_slave)
            l =[]
            for i in x['items']:
                try:
                    n=i.get('media').get('code')
                except:
                    n = i.get("channel").get('media').get('code')
                l.append(n)
            ShortCode.objects.bulk_create([ShortCode(iguser=y,code=code) for code in l])
        except Exception as e:
            Status.objects.create(ig_id=y,comment="SOME THING WENT WRONG IN GET SHORTCODE",response=e,status="Fail")

        
