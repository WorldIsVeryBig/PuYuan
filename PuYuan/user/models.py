from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
class UserProfile(AbstractUser):
    phone = models.CharField(max_length=100, blank=True)
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank= True, unique= True)
    email  = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=100,blank=True)
    account = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        data = dict()
        data = {
            'uid':self.uid,
            'id':self.id,
            'phone':self.phone,
            'email':self.email,
            'username':self.username,
            'password':self.password,
            'account':self.account,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
        }
        return str(data)

class UserSet(models.Model):
    uid = models.CharField(max_length=100, blank=True)          #使用者的token 串連方式
    name  = models.CharField(max_length=100,blank=True)          #使用者的暱稱
    birthday  = models.DateField(blank=True,null=True)      #使用者生日
    height  = models.DecimalField(max_digits=19,decimal_places=16,blank=True,null=True)        #使用者的身高
    gender  = models.CharField(max_length=100,blank=True)        #使用者的性別 0=男生 , 1=女生
    fcm_id  = models.CharField(max_length=100,blank=True)
    address  = models.CharField(max_length=100,blank=True)       #使用者的居住地址
    weight  = models.DecimalField(max_digits=19,decimal_places=16,blank=True,null=True)        #使用者的體重
    phone  = models.CharField(max_length=100,blank=True)         #使用者的電話
    email  = models.CharField(max_length=100,blank=True)         #使用者的郵件
    created_at = models.DateTimeField(auto_now_add=True)        #建立時間
    updated_at = models.DateTimeField(auto_now=True)            #資料上傳時間
    pushed_at = models.DateTimeField(auto_now=True)             #news最新資料時間
    unread_records_one =  models.DecimalField(max_digits=10,decimal_places=0,default=0)
    unread_records_two =  models.CharField(max_length=100,blank=True,default='0')
    unread_records_three =  models.DecimalField(max_digits=10,decimal_places=0,default=0)
    verified =models.CharField(max_length=10,default="0")
    privacy_policy =models.CharField(max_length=10,default="0")
    must_change_password = models.BooleanField(default=False)
    status = models.CharField(max_length=100,default="Normal")
    login_times = models.DecimalField(max_digits=15,decimal_places=0,default="0")
    after_recording = models.CharField(max_length=1,default='0')
    no_recording_for_a_day = models.CharField(max_length=1,default='0')
    over_max_or_under_min =models.CharField(max_length=1,default='0')
    after_mael = models.CharField(max_length=1,default='0')
    unit_of_sugar = models.CharField(max_length=1,default='0')
    unit_of_weight = models.CharField(max_length=1,default='0')
    unit_of_height =models.CharField(max_length=1,default='0')
    badge = models.DecimalField(max_digits=15,decimal_places=0,default="0")
    group = models.CharField(max_length=100,blank=True)
    def __str__(self):
        data = list()
        data = {
            'uid':self.uid,
            'name':self.name,
            'birthday':self.birthday,
            'height':self.height,
            'gender':self.gender,
            'fcm_id':self.fcm_id,
            'address':self.address,
            'weight':self.weight,
            'phone':self.phone,
            'email':self.email,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
            'verified':self.verified,
            'privacy_policy':self.privacy_policy,
            'must_change_password':self.must_change_password,
            'login_times':self.login_times,
            'status':self.status,
            'badge':self.badge,
            'group':self.group,

        }
        return str(data)
class set_default(models.Model):
    uid = models.CharField(max_length=100, blank=True)
    sugar_delta_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    sugar_delta_min  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    sugar_morning_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    sugar_morning_min  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    sugar_evening_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    sugar_evening_min  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    sugar_before_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    sugar_before_min  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    sugar_after_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    sugar_after_min  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    systolic_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    systolic_min  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    diastolic_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    diastolic_min  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    pulse_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    pulse_min =  models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    weight_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    weight_min  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    bmi_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    bmi_min  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    body_fat_max  = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    body_fat_min = models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        data = list()
        data = {
            'uid':self.uid,
            'sugar_delta_max':self.sugar_delta_max,
            'sugar_delta_min':self.sugar_delta_min,
            'sugar_morning_max':self.sugar_morning_max,
            'sugar_morning_min':self.sugar_morning_min,
            'sugar_evening_max':self.sugar_evening_max,
            'sugar_evening_min':self.sugar_evening_min,
            'sugar_before_max':self.sugar_before_max,
            'sugar_before_min':self.sugar_before_min,
            'sugar_after_max':self.sugar_after_max,
            'sugar_after_min':self.sugar_after_min,
            'systolic_max':self.systolic_max,
            'systolic_min':self.systolic_min,
            'diastolic_max':self.diastolic_max,
            'diastolic_min':self.diastolic_min,
            'pulse_max':self.pulse_max,
            'pulse_min':self.pulse_min,
            'weight_max':self.weight_max,
            'weight_min':self.weight_min,
            'bmi_max':self.bmi_max,
            'bmi_min':self.bmi_min,
            'body_fat_max':self.body_fat_max,
            'body_fat_min':self.body_fat_min,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(data)
class Notification(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    member_id = models.CharField(max_length = 100,blank=True)
    reply_id = models.CharField(max_length = 100,blank=True)
    message = models.CharField(max_length = 100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'member_id':self.member_id,
            'reply_id':self.reply_id,
            'message':self.message,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(message)
class HbA1c(models.Model):
    uid = models.CharField(max_length=100, blank=True)
    a1c = models.DecimalField(max_digits=6,decimal_places=0,blank=True,null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        data = dict()
        data = {
            'uid':self.uid,
            'a1c':self.a1c,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(data)
class medicalinformation(models.Model):
    uid = models.CharField(max_length=100, blank=True)
    user_id =  models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    diabetes_type =  models.DecimalField(max_digits=15,decimal_places=0,default=0)
    oad = models.CharField(max_length=1, default='0')
    insulin = models.CharField(max_length=1, default='0')
    anti_hypertensivers = models.CharField(max_length=1, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        medata = dict()
        medata = {
            'uid':self.uid,
            'user_id':self.user_id,
            'oad':self.oad,
            'insulin':self.insulin,
            'anti_hypertensivers':self.anti_hypertensivers,
            'diabetes_type':self.diabetes_type,
            'created_at':self.created_at,
            'updated_at':self.updated_at
            
        }
        return str(medata)
class druginformation(models.Model):
    uid = models.CharField(max_length=100, blank=True)
    drugname =  models.CharField(max_length=50, blank=True,null=True)
    drugtype = models.CharField(max_length=1, default='0')
    recorded_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        data = dict()
        data = {
            'uid':self.uid,
            'drugname':self.drugname,
            'drugtype':self.drugtype,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(data)
class Share(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    fid = models.CharField(max_length = 100,blank=True)
    data_type = models.CharField(max_length = 100,blank=True)
    relation_type = models.CharField(max_length = 100,blank=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'fid':self.fid,
            'data_type':self.data_type,
            'relation_type':self.relation_type
        }
        return str(message)