import subprocess
import time
import threading
from core.functions import end_broadcast, get_shortcode_from_explore, get_shortcode_from_reels_2, get_user_by_id, get_users_from_shortcode, start, start_broadcast
from core.models import IgUser, Status
import random


class InstaGetUserThread(threading.Thread):
    def __init__(self, user_id):
        self.user_id = user_id
        threading.Thread.__init__(self)

    def run(self):
        y = IgUser.objects.get(id=self.user_id)
        random_bit = random.getrandbits(1)
        random_boolean = bool(random_bit)
        try:
            if random_boolean:
                print("------------- SHORTCODE FROM REELS -------------")
                x = get_shortcode_from_reels_2(user=y)
            else:
                print("------------- SHORTCODE FROM EXPLORE -------------")
                x = get_shortcode_from_explore(cookie=y.cookie)
        except:
            x = get_shortcode_from_explore(cookie=y.cookie)
        try:
            lis = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            x = x['items'][random.choice(lis)]['media']['code']
        except KeyError:
            lis = [0, 1, 2, 3, 4]
            x = x['items'][random.choice(lis)]['media']['code']
        except:
            x = x['items'][0]['media']['code']
        try:

            x = get_users_from_shortcode(cookie=y.get_slave, shortcode=x)
            y = IgUser.objects.get(id=y.id)
            y.desc = y.desc+",".join(x)+","
            y.save()
        except Exception as x:
            Status.objects.create(status='Fail', ig_id=y,
                                  comment=x, response="FAILED TO FETCH USERS")


class IVThread(threading.Thread):
    def __init__(self, user, ids):
        self.user = user
        self.ids = ids
        threading.Thread.__init__(self)

    def run(self):
        try:
            print(self.ids)
            j = get_user_by_id(user=self.user, user_id=self.ids)
           
            time.sleep(2)
        except:
            print("===========ERROR===========")
            # pass


class InstaInviteThread(threading.Thread):
    def __init__(self, user_id):
        self.user_id = user_id
        threading.Thread.__init__(self)

    def run(self):
        y = IgUser.objects.get(id=self.user_id)
        start_broadcast(user=y)
        time.sleep(2)
        print("----------------INVITE--------------------")
        try:
            x = y.desc
            x = str(x).split(',')
            test_list = list(set([int(i) for i in x if bool(i)]))
            n = 400
            output = [test_list[i:i + n] for i in range(0, len(test_list), n)]
            #   json.loads(y.json)
            threads = []
            for max in output:
                print(len(max))
                if len(max) < 1:
                    print("FAILED TO CONTINUE")
                    continue

                max.append(4619342150)
                d = [str(i) for i in set(max)]
                l = ",".join(d)
                IVThread(user=y, ids=l).start()
            print("GOING TO END")
            IgUser.objects.filter(username=y.username,
                                  active=True).update(desc="4619342150,")
            time.sleep(40)
            end_broadcast(user=y)
            print("__________________ENDING LIVE__________________")
            
            Status.objects.create(ig_id=y, comment=output,
                                  response="PROCESSING")
            start(user=y)
        except Exception as e:
            Status.objects.create(
                ig_id=y, comment="SOME THING WENT WRONG IN INVITE", response=e, status="Fail")


class LiveStreamThread(threading.Thread):
    def __init__(self, user_id):
        self.user_id = user_id
        threading.Thread.__init__(self)

    def run(self):
        user = IgUser.objects.get(id=self.user_id)
        print("----------------STREAMING--------------------")
        file = "out.avi"
        start_broadcast(user=user)
        url = user.live_url
        """
        ffmpeg -re -i "kk.mp4" -vcodec libx264 -preset:v ultrafast -acodec aac -f flv  "rtmps://live-upload.instagram.com:443/rtmp/17964238498490510?s_sw=0&s_vt=ig&a=Abwh05f79YgxruUE"
        """
        ffmpeg_cmd = f'ffmpeg -stream_loop 3 -re -i "{file}" -profile:v baseline -s 720x1280 -vcodec libx264 -preset:v ultrafast -acodec aac -f flv  "{url}"'

        # ffmpeg_cmd = f'ffmpeg -rtbufsize 256M -re -i "{file}" -acodec libmp3lame -ar 44100 -b:a 128k -pix_fmt yuv420p -profile:v baseline -s 720x1280 -bufsize 6000k -vb 400k -maxrate 1500k -deinterlace -vcodec libx264 -preset veryfast -g 30 -r 30 -f flv "{url}"'
        # print(ffmpeg_cmd)
        subprocess.call(ffmpeg_cmd, shell=True)
