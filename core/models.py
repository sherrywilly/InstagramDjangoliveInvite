import random
from uuid import uuid4
from django.db import models
from django.urls import reverse

# Create your models here.


class SlaveUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    cookie = models.JSONField(blank=True, null=True)
    pro_pic = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.CharField(blank=True, null=True, max_length=50)

    def __str__(self):
        return self.username


class IgUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4,
                          editable=False, unique=True)
    username = models.CharField(unique=True, max_length=200)
    password = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    ftime = models.TimeField(blank=True, null=True, verbose_name="From Time")
    ttime = models.TimeField(blank=True, null=True, verbose_name="To Time",)
    cookie = models.JSONField(blank=True, null=True)
    pro_pic = models.CharField(blank=True, null=True, max_length=500)
    b_id = models.CharField(null=True, blank=True, max_length=50)
    slave = models.ForeignKey(
        SlaveUser, on_delete=models.SET_NULL, blank=True, null=True)
    counter = models.IntegerField(default=0)
    counter2 = models.IntegerField(default=0)
    desc = models.TextField(verbose_name="description mentions",default="",blank=True,null=True)
    comment = models.CharField(
        max_length=500, blank=True, null=True, default="FOLLOW ME🌟🌟 FOLLOW BACK SURE👍  ")
    proxy = models.CharField(max_length=100,blank=True,null=True,verbose_name="proxy",help_text="https://username:password@ip:port")

    @property
    def get_desc(self):
        x= f"HEY FOLLOW ME 👉 @{self.username} ❤️CHECK MY PROFILE 🤗FOLLOW BACK SURE 💯STAY SAFE 👉 @{self.username}  • • • • • • • • • • • • • •  • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • • • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •  • • • • • • • • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •• • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •    • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •    • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •    • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •     • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •  • • • • • • • • • • • • • •  • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • • • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •  • • • • • • • • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •• • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •    • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •    • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •    • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •     • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • • • • • • • • •  • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • • • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •  • • • • • • • • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •• • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •    • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •    • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •    • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •     • • • • • • • • • • • • • •   • • • • • • •  • • • • • • •   • • • • • • •   • • • • • • •   • • • • • • •  {self.desc} @codermallu"
        return x
    @property
    def get_slave(self):

        if self.slave is not None:
            return self.slave.cookie
        elif SlaveUser.objects.filter(created_by=self.username).exists() and self.slave is None:
            _x = SlaveUser.objects.filter(created_by=self.username)
            _count = random.randint(0, _x.count()-1)
            return _x[_count].cookie
        else:
            return self.cookie

        return self.cookie

    def get_login_url(self):
        return reverse("iglogin", kwargs={"id": self.pk})

    def __str__(self):
        return self.username+"  "+str(self.active)

    def total_count(self):
        try:
            c = self.status_set.all().count()
        except:
            c = 0
        return c

    def success_count(self):
        try:
            c = self.status_set.filter(status__iexact="success").count()
        except:
            c = 0
        return c

    def fail_count(self):
        try:
            c = self.status_set.filter(status__icontains="fail").count()
        except:
            c = 0
        return c

    @property
    def get_shortcode(self):
        return self.shortcode.first()

    # @property
    # def tags(self):
    #     x = [i.name for i in self.tag_set.all()]
    #     if len(x) > 0:
    #         return x
    #     else:
    #         x = ['india', 'kerala', 'mallu', 'malappuram', 'kochi']
    #         return x


class Status(models.Model):
    ig_id = models.ForeignKey(IgUser, on_delete=models.CASCADE)
    status = models.CharField(default="Success", max_length=20)
    comment = models.TextField(blank=True,null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    response = models.JSONField(blank=True, null=True)

    def __str__(self):
        return str(self.ig_id.username)+" "+self.status+"  "+str(self.datetime)

    class Meta:
        ordering = ['-datetime', ]


# class Tag(models.Model):
#     iuser = models.ForeignKey(IgUser, on_delete=models.CASCADE)
#     name = models.CharField(max_length=10)

#     def __str__(self):
#         return str(self.iuser.username)+" "+self.name


class TargetUsers(models.Model):
    pass

class ShortCode(models.Model):
    iguser = models.ForeignKey(IgUser,on_delete=models.CASCADE,related_name="shortcode")
    code = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}  {self.iguser}"
