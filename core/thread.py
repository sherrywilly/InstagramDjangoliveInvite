import threading

from django.db import transaction
from core.functions import get_shortcode_from_explore, get_shortcode_from_reels_2, get_user_by_id, get_users_from_shortcode

from core.models import IgUser, Status
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
            
            random_bit = random.getrandbits(1)
            random_boolean = bool(random_bit)
            if random_boolean:
                print("------------- SHORTCODE FROM REELS -------------")
                x = get_shortcode_from_reels_2(user=y)
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