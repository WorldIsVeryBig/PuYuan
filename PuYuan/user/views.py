from friend.models import *
from body.models import *
import re
from django.core.checks import messages
from django.http.response import HttpResponse
from .token import email_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from PuYuan import settings
from django.shortcuts import render
from django.http import JsonResponse, request
from .models import *
from django.core.mail import send_mail
import json, uuid, base64, string
from django.contrib.auth import authenticate , login , logout
from django.contrib.sessions.models import Session
from django.shortcuts import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from .models import UserProfile
from datetime import datetime
import random
from friend.models import *
from .forms import PersonalDefaultForm
from urllib.parse import unquote
# Create your views here.
@csrf_exempt
def register(request):              #註冊 #OK
    if request.method == "POST":
        data = request.body
        data = str(data,encoding="utf-8").replace("%40","@")
        a = re.split("=|&",str(data))
        try:
            account= a[1]
            # phone= data["phone"]
            email= a[3]
            password= a[5]
            uid=uuid.uuid3(uuid.NAMESPACE_DNS,account)
            time= datetime.now()
            date_time = time.strftime("%Y-%m-%d %H:%M:%s")
            user = UserProfile.objects.create_user(username=account, email=email, uid=uid,account=account)
            user.set_password(password)
            user.save()
            P_id = UserProfile.objects.get(uid = uid)
            id_number = P_id.uid
            a="0123456789"
            invite_code = "".join( random.sample(a,8))
            user= UserSet.objects.create(uid=uid,name=account,privacy_policy=0,email=email,must_change_password=False,login_times=0,created_at=date_time,updated_at=date_time)
            set_default.objects.create(uid=uid,created_at=date_time,updated_at=date_time)
            Friend.objects.create(uid = id_number, invite_code = invite_code )
            Notification.objects.create(uid = uid)
            HbA1c.objects.create(uid=uid)
            message={'status':'0'}
        except Exception as e:
            print(e)
            message={"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def login_request(request):         #登入 #OK
    if request.method == "POST":
        data = request.body
        data = str(data,encoding="utf-8").replace("%40","@")
        a = re.split("=|&",str(data))
        try:
            account = a[1]
            password = a[5]
            auth_obj = auth.authenticate(username=account, password=password)
            if auth_obj:
                request.session.create()
                auth.login(request, auth_obj)
            message = {"status": "0",
            "token":request.session.session_key
            }
        except Exception as e:
            print(e)
            message= {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def logout_request(request):        #登出 #OK
    try:
        auth.logout(request)
        message = {"status":"0"}
        return HttpResponseRedirect('api/login')
    except:
        message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def send(request):                  #發送驗證信 #OK
    if request.method == "POST":
        data = request.body
        data = str(data,encoding="utf-8").replace("%40","@")
        try:
            token = email_token()
            receiver = str(data).split("=")[1]
            verification_code = token.generate_validate_token(receiver)
            sender = settings.EMAIL_HOST_USER
            title = "普元血糖帳號驗證"
            meg ="\n".join(["{0}歡迎使用普元血糖app".format(receiver),
            "請訪問該連結，完成使用者驗證:","/".join(['192.168.1.133:8000/api/check',verification_code])])
            send_mail(title,meg,sender,[receiver])
            messenge={"status":"0"}
        except:
            messenge={"status":"1"}
        return JsonResponse(messenge)
@csrf_exempt
def check(request,token):       #驗證驗證碼 #OK
    if request.method == "POST":
        data = request.body
        data = str(data, encoding='utf-8')
        try:
            email = data['email']
            check_token = email_token()
            email = check_token.confirm_validate_token(token)
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            messenge={"status":"0"}
        except:
            messenge={"status":"1"}
        return JsonResponse(messenge)
@csrf_exempt
def password_forgot(request):       #忘記密碼 #ok
    if request.method == "POST":
        data = request.body
        data = str(data,encoding="utf-8").replace("%40","@")
        a = re.split("=|&",str(data))
        try:
            email = a[1]
            user = UserProfile.objects.filter(email=email)
            a="abcdefghijklmnopqrstuvwxyz0123456789"
            newpassword = "".join( random.sample(a,8))
            update = user.update(password = newpassword)
            receiver = email
            sender = settings.EMAIL_HOST_USER
            title = '普元密碼驗證'
            meg ="\n".join(["歡迎".format(receiver),
            "新的密碼為:\n",newpassword])
            send_mail(title,meg,sender,[receiver])
            messenge={"status":"0"}
        except Exception as e:
            print(e)
            messenge={"status":"1"}
        return JsonResponse(messenge)
@csrf_exempt
def reset_password(request):        #重設密碼 #OK
    if request.method == "POST":
        data = request.body
        data = str(data, encoding="UTF-8")
        a= data.split("=")
        try:
            s = Session.objects.get(
            pk=request.META.get('HTTP_COOKIE','')[-32:]).get_decoded()
            user = UserProfile.objects.get(id=s['_auth_user_id'])
            userset = UserSet.objects.get(uid=user.uid)
            new_password = a[1]
            user.set_password(new_password)
            userset.must_change_password = False
            user.save()
            userset.save()
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def register_check(request):    #註冊確認 #OK
    if request.method == "GET":
        try:
            user_exist = request.GET["account"]
            message = {"status":"0"}
        except:
            message = {"status":"1"}
    return JsonResponse(message)
@csrf_exempt
def user_set(request):      #個人資訊設定
    if request.method == "PATCH":
        data = request.body
        data = str(data,encoding="UTF-8").replace("%40","@")
        a = re.split("=|&",str(data))
        user = UserSet.objects.get(uid = request.user.uid)
        try:
            user.name = a[11]
            user.birthday = a[3]
            user.height = a[9]
            user.gender = a[7]
            user.address = a[1]
            user.weight = a[15]
            user.phone = a[13]
            user.fcm_id = a[1]
            user.email = a[5]
            user.save()
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)

    if request.method == "GET":     # 個人設定展示
        data = request.body
        data = str(data, encoding='UTF-8')
        try:
            s = Session.objects.all()[0]
            s.expire_date
            s = Session.objects.get(
                pk=request.META.get('HTTP_COOKIE','')[-32:]).get_decoded()
            UserProfiledata = UserProfile.objects.get(id=s['_auth_user_id'])
            UserSetdata = UserSet.objects.get(uid=UserProfiledata.uid)
            Userdeflat = set_default.objects.get(uid=UserProfiledata.uid)
            messages = {
            "status":"0",
            
            "user":{
            "id":UserProfiledata.id,
            "name":UserSetdata.name,
            "account":UserProfiledata.account,
            "email":UserProfiledata.email,
            "phone":UserProfiledata.phone,
            "status":UserSetdata.status,
            "group":UserSetdata.group,
            "birthday":UserSetdata.birthday,
            "height":UserSetdata.height,
            "weight":UserSetdata.weight,
            "gender":UserSetdata.gender,
            "address":UserSetdata.address,
            "unread_records":[int(UserSetdata.unread_records_one),UserSetdata.unread_records_two,int(UserSetdata.unread_records_three)],
            "verified":int(UserSetdata.verified),
            "privacy_policy":UserSetdata.privacy_policy,
            "must_change_password":1 if UserSetdata.must_change_password else 0,
            "fcm_id":UserSetdata.fcm_id,
            "badge":int(UserSetdata.badge),
            "login_time":int(UserSetdata.login_times),
            "created_at": datetime.strftime(UserSetdata.created_at,"%Y-%m-%D %H:%M:%S"),
            "updated_at": datetime.strftime(UserSetdata.updated_at,"%Y-%m-%D %H:%M:%S")},
            "default":{
            "id": UserProfiledata.id,
            "user_id": Userdeflat.uid,
            "sugar_delta_max": int(Userdeflat.sugar_delta_max),
            "sugar_delta_min":int(Userdeflat.sugar_delta_min),
            "sugar_morning_max": int(Userdeflat.sugar_morning_max),
            "sugar_morning_min": int(Userdeflat.sugar_morning_min),
            "sugar_evening_max": int(Userdeflat.sugar_evening_max),
            "sugar_evening_min": int(Userdeflat.sugar_evening_min),
            "sugar_before_max": int(Userdeflat.sugar_before_max),
            "sugar_before_min": int(Userdeflat.sugar_before_min),
            "sugar_after_max": int(Userdeflat.sugar_after_max),
            "sugar_after_min":int(Userdeflat.sugar_after_min),
            "systolic_max": int(Userdeflat.systolic_max),
            "systolic_min": int(Userdeflat.systolic_min),
            "diastolic_max": int(Userdeflat.diastolic_max),
            "diastolic_min":int(Userdeflat.diastolic_min),
            "pulse_max": int(Userdeflat.pulse_max),
            "pulse_min":int(Userdeflat.pulse_min),
            "weight_max": int(Userdeflat.weight_max),
            "weight_min": int(Userdeflat.weight_min),
            "bmi_max": int(Userdeflat.bmi_max),
            "bmi_min": int(Userdeflat.bmi_min),
            "body_fat_max": int(Userdeflat.body_fat_max),
            "body_fat_min": int(Userdeflat.body_fat_min),
            "created_at": datetime.strftime(UserSetdata.created_at ,"%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.strftime(UserSetdata.updated_at,"%Y-%m-%d %H:%M:%S")},
            
            "setting":{
            "id": UserProfiledata.id,
            "user_id":UserProfiledata.uid,
            "after_recording": int(UserSetdata.after_recording),
            "no_recording_for_a_day": int(UserSetdata.no_recording_for_a_day),
            "over_max_or_under_min": int(UserSetdata.over_max_or_under_min),
            "after_meal":int(UserSetdata.after_mael),
            "unit_of_sugar": int(UserSetdata.unit_of_sugar),
            "unit_of_weight": int(UserSetdata.unit_of_weight),
            "unit_of_height": int(UserSetdata.unit_of_height),
            "created_at":datetime.strftime(UserSetdata.created_at ,"%Y-%m-%D %H:%M:%S"),
            "updated_at": datetime.strftime(UserSetdata.updated_at ,"%Y-%m-%D %H:%M:%S")
            }}
            message = messages
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def user_default(request):      #個人預設值
    if request.method == "PATCH":
        data = request.body
        data = str(data, encoding="UTF-8")
        user = set_default.objects.get(uid = request.user.uid)
        try:
            f = PersonalDefaultForm(data)
            if f.is_valid():
                data = f.cleaned_data
                filtered = {i: data[i] for i in data if data[i]}
                if filtered:
                    for i in filtered:
                        setattr(user, i, filtered[i])
                    user.save()
            message = {"stasus":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def userdata(request):
    if request.method == 'PATCH':  #個人設定上傳
        data = request.body
        data = str(data, encoding="utf-8")
        user = UserSet.objects.get(uid=request.user.uid)
        try:
            user.after_recording = data['after_recording']
            user.no_recording_for_a_day = data['no_recording_for_a_day']
            user.over_max_or_under_min = data['over_max_or_under_min']
            user.after_mael = data['after_mael']
            user.unit_of_sugar = data['unit_of_sugar']
            user.unit_of_weight = data['unit_of_weight']
            user.unit_of_height = data['unit_of_height']
            user.save()
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def notification(request):      # 親友團通知
    if request.method == "POST":
        data = request.body
        data = str(data, encoding="UTF-8")
        uid = request.user.uid
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            message = data['message']
            friend_list = Friend_data.objects.filter(uid=uid, friend_type=1, status=1)
            for friend in friend_list:
                Notification.objects.create(uid=uid, member_id=1, reply_id=friend.relation_id, message=message, updated_at=nowtime)
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def ShowHbA1c(request):         #展示醣化血色素
    if request.method == "GET":
        uid = request.user.uid
        try:
            HbA1cdata = HbA1c.objects.filter(uid=uid)
            UserProfiledata = UserProfile.objects.get(uid=uid)
            datas = []
            for HbA1cdata_list in HbA1cdata:
                datas.append({
                "id":HbA1cdata_list.id,
                "user_id":UserProfiledata.id,
                "a1c":str(HbA1cdata_list.a1c),
                "created_at":datetime.strftime(HbA1cdata_list.created_at ,"%Y-%m-%d %H:%M:%S"),
                "updated_at":datetime.strftime(HbA1cdata_list.updated_at ,"%Y-%m-%d %H:%M:%S"),
                "recorded_at":datetime.strftime(HbA1cdata_list.recorded_at ,"%Y-%m-%d %H:%M:%S")
                })
            
            message = {
            "status":"0",
            "a1cs":datas}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)

    if request.method == "POST":    #醣化血色素資訊上傳
        data = request.body
        data = str(data, encoding="UTF-8").replace("%20"," ").replace("%3A",":")
        a = re.split("=|&",str(data))
        uid = request.user.uid
        try:
            user = HbA1c.objects.filter(uid=uid)
            b = a[1]
            a1c = user.a1c = int(b)
            recorded_at = user.recorded_at = a[3]
            HbA1c.objects.create(uid = uid ,a1c = a1c, recorded_at = recorded_at )
            message = {"status":"0"}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)

    if request.method =="DELETE":   #醣化血色素資訊刪除
        data = request.body
        data = str(data,encoding= "UTF-8")
        uid = request.user.uid
        try:
            user = HbA1c.objects.filter(uid = uid)
            if user:
                user.delete()
            message = {"status":"0"}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def Medical_information(request):
    if request.method == "GET":   #就醫資訊
        data = request.body
        data = str(data,encoding="UTF-8")
        uid = request.user.uid
        try:
            MedicalInformation = medicalinformation.objects.get(uid = uid)
            UserProfileData = UserProfile.objects.get(uid = uid)
            
            message = {"status":"0",
                        "medical_info":[{
            "id":int(UserProfileData.id),
            "user_id":MedicalInformation.user_id,
            "diabetes_type":int(MedicalInformation.diabetes_type),
            "oad":int(MedicalInformation.oad),
            "insulin":int(MedicalInformation.insulin),
            "anti_hypertensivers":int(MedicalInformation.anti_hypertensivers),
            "created_at":datetime.strftime(UserProfileData.created_at ,"%Y-%m-%d %H:%M:%S"),
            "updated_at":datetime.strftime(UserProfileData.updated_at ,"%Y-%m-%d %H:%M:%S")
            }]}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
    if request.method == "PATCH":   #更新就醫資訊
        data = request.body
        data = str(data,encoding="UTF-8")
        uid = request.user.uid
        try:
            medicalinformations = medicalinformation.objects.get(uid = uid)
            medicalinformations.user_id = data["user_id"]
            medicalinformations.diabetes_type = data["diabetes_type"]
            medicalinformations.oad = data["oad"]
            medicalinformations.insulin = data["insulin"]
            medicalinformations.anti_hypertensivers = data["anti_hypertensivers"]
            medicalinformations.save()
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def drug(request):
    data = request.body
    data = str(data, encoding="UTF-8").replace("%20"," ").replace("%3A",":")
    uid = request.user.uid
    a = re.split("=|&",str(data))
    if request.method == "GET":     #藥物資訊
        try:
            DrugInformationData = druginformation.objects.filter(uid = uid)
            UserSetData = UserSet.objects.get(uid = uid)
            for DrugInformationData_list in DrugInformationData:
                drugtype = DrugInformationData_list.drugtype
                if str(drugtype) == "0":
                    message = {"status":"0",
                                "drug_useds":[{
                    "id":DrugInformationData_list.id,
                    "user_id":UserSetData.name,
                    "type":DrugInformationData_list.drugtype,
                    "name":DrugInformationData_list.drugname,
                    "recorded_at":DrugInformationData_list.recorded_at
                    }]}
                elif str(drugtype) == "1":
                    message = {"status":"0",
                                "drug_useds":[{
                    "id":DrugInformationData_list.id,
                    "user_id":UserSetData.name,
                    "type":DrugInformationData_list.drugtype,
                    "name":DrugInformationData_list.drugname,
                    "recorded_at":DrugInformationData_list.recorded_at
                    }]}
                else:
                    message = {"status":"查無資料。"}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)

    if request.method == "POST":        #上傳藥物資訊
        try:
            de_1 = unquote(a[1],'UTF-8')
            user = druginformation.objects.filter(uid = uid)
            time = datetime.now()
            timeprint = datetime.strftime(time,"%Y-%m-%d %H:%M:%S")
            str(timeprint)
            drugtype = a[5]
            drugname = de_1
            updated_at = timeprint
            druginformation.objects.create(uid = uid, drugname = drugname, drugtype = drugtype, updated_at = updated_at)
            message = {"status":"0"}
        except Exception as e :
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
    if request.method == "DELETE":      #刪除藥物資訊
        try:
            data = request.body
            user = druginformation.objects.filter(uid = uid)
            DeleteWho = request.GET.getlist("ids[]")
            if DeleteWho == ['1']:
                user.drugtype = ""
                user.save()
            elif DeleteWho == ['2']:
                user.drugname = ""
                user.save()
            elif DeleteWho == ['1','2']:
                user.drugname = ""
                user.drugtype = ""
                user.save()
            message = {"status":"0"}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def badge(request):
    if request.method == 'PUT': #更新badge #ok
            data = request.body
            data = str(data, encoding="utf-8")
            data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
            }

            s = Session.objects.get(
            pk=request.META.get('HTTP_COOKIE','')[-32:]).get_decoded()

            UserProfiledata = UserProfile.objects.get(id=s['_auth_user_id'])
            user = UserSet.objects.get(uid=UserProfiledata.uid)
            try:
                user.badge = data['badge']
                user.save()
                status = {"status":"0"}
            except:
                status = {"status":"1"}

            return JsonResponse(status)
@csrf_exempt
def newnews(request): #最新消息 #ok
    if request.method == 'GET':
        uid = request.user.id
        user = UserProfile.objects.get(id=uid)
        UserSetdata = UserSet.objects.get(uid=user.uid)
        Notificationdata = Notification.objects.get(uid=UserSetdata.uid)

        try:
            message = {
            'status':'0',
            'news':{
                "id": 2,
                "member_id": 1,
                "group": 1,
                "message": "456",
                "pushed_at": "2017-11-16 16:33:06",
                "created_at": datetime.strftime(UserSetdata.created_at ,"%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.strftime(UserSetdata.updated_at ,"%Y-%m-%d %H:%M:%S")
                }
            }
        except:
            message = {'status':'1'}
        
        return JsonResponse(message)
@csrf_exempt
def share(request): # 分享!
    uid = request.user.id
    if request.method == 'POST':
        data = request.POST.dict()
        share_id = data['id']
        data_type = data['type']
        relation_type = data['relation_type']
        try:
            Share.objects.create(uid=uid, fid=share_id, data_type=data_type, relation_type=relation_type)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}
        return JsonResponse(output,safe=False)

@csrf_exempt
def share_check(request,relation_type): # 查看分享（含自己分享出去的）!
    uid = request.user.uid
    if request.method == 'GET':
        if Share.objects.filter(relation_type=relation_type):
            share_checks = Share.objects.filter(relation_type=relation_type, uid = uid)
            datas = []
            for share_check in share_checks:
                if share_check.uid != uid:
                    Friend_data.objects.get(uid=uid, relation_id=share_check.uid, status=1, friend_type=relation_type)
                    user_pro = UserProfile.objects.get(id=share_check.uid)
                    user = UserSet.objects.get(uid=user_pro.uid)
                else:
                    user_pro = UserProfile.objects.get(uid=uid)
                    user = UserSet.objects.get(uid=user_pro.uid)
                if share_check.data_type == '0' :
                    share_data = Blood_pressure.objects.filter(uid=share_check.uid)
                    created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
                    r = {
                        "id":share_data.id,
                        "user_id":share_data.uid,
                        "systolic":share_data.systolic,
                        "diastolic":share_data.diastolic,
                        "pulse":share_data.pulse,
                        "recorded_at":recorded_at,
                        "created_at":created_at,
                        "type":0,
                        "user":{
                            "id":user_pro.uid,
                            "name":user.name,
                            "account":user.email,
                            "email":user.email,
                            "phone":user.phone,
                            "fb_id":user_pro.fb_id,
                            "status":user.status,
                            "group":user.group,
                            "birthday":user.birthday,
                            "height":user.height,
                            "gender":user.gender,
                            "verified":user.verified,
                            "privacy_policy":user.privacy_policy,
                            "must_change_password":user.must_change_password,
                            "badge":user.badge,
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                            }
                        }
                if share_check.data_type == '1' :
                    share_data = Weight.objects.filter(uid=share_check.uid)
                    created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
                    r = {
                        "id":share_data.id,
                        "user_id":share_data.uid,
                        "weight":float(share_data.weight),
                        "body_fat":float(share_data.body_fat),
                        "bmi":float(share_data.bmi),
                        "recorded_at":recorded_at,
                        "created_at":created_at,
                        "type":1,
                        "user":{
                            "id":user_pro.uid,
                            "name":user.name,
                            "account":user.email,
                            "email":user.email,
                            "phone":user.phone,
                            "fb_id":user_pro.fb_id,
                            "status":user.status,
                            "group":user.group,
                            "birthday":user.birthday,
                            "height":user.height,
                            "gender":user.gender,
                            "verified":user.verified,
                            "privacy_policy":user.privacy_policy,
                            "must_change_password":user.must_change_password,
                            "badge":user.badge,
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                            }
                        }
                if share_check.data_type == '2' :
                    share_data = Blood_sugar.objects.filter(uid=share_check.uid)
                    for share_data_list in share_data:
                        created_at = datetime.strftime(share_data_list.created_at, '%Y-%m-%d %H:%M:%S')
                        recorded_at = datetime.strftime(share_data_list.recorded_at, '%Y-%m-%d %H:%M:%S')
                        created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
                        updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
                        r = {
                            "id":share_data_list.uid,
                            "user_id":share_data_list.uid,
                            "sugar":float(share_data_list.sugar),
                            "timeperiod":int(share_data_list.timeperiod),
                            "recorded_at":recorded_at,
                            "created_at":created_at,
                            "type":2,
                            "user":{
                                "id":user_pro.id,
                                "name":user.name,
                                "account":user.email,
                                "email":user.email,
                                "phone":user.phone,
                                "status":user.status,
                                "group":user.group,
                                "birthday":user.birthday,
                                "height":user.height,
                                "gender":user.gender,
                                "verified":user.verified,
                                "privacy_policy":user.privacy_policy,
                                "must_change_password":user.must_change_password,
                                "badge":user.badge,
                                "created_at":created_at_userfile,
                                "updated_at":updated_at_userfile
                                }
                            }
                if share_check.data_type == '3' :
                    share_data = Diary_diet.objects.filter(uid=share_check.uid)
                    created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
                    image = str(share_data.image)
                    r = {
                        "id":share_data.id,
                        "user_id":share_data.uid,
                        "description":share_data.description,
                        "meal":int(share_data.meal),
                        "tag":share_data.tag,
                        "image":str(image),
                        "lat":share_data.lat,
                        "lng":share_data.lng,
                        "recorded_at":recorded_at,
                        "created_at":created_at,
                        "type":3,
                        "user":{
                            "id":user_pro.uid,
                            "name":user.name,
                            "account":user.email,
                            "email":user.email,
                            "phone":user.phone,
                            "fb_id":user_pro.fb_id,
                            "status":user.status,
                            "group":user.group,
                            "birthday":user.birthday,
                            "height":user.height,
                            "gender":user.gender,
                            "verified":user.verified,
                            "privacy_policy":user.privacy_policy,
                            "must_change_password":user.must_change_password,
                            "badge":user.badge,
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                            }
                        }
                else :
                    r = {}
            datas.append(r)
            output = {"status":"0", "records":datas}
        else:
            output = {"status":"1"}
        return JsonResponse(output)