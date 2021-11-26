from datetime import date
import re
from django.core.checks import messages
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib import auth
from .models import *
from urllib.parse import unquote
import json
from datetime import datetime
from friend.models import *

# Create your views here.
@csrf_exempt
def blood_pressure(request):    # 上傳血壓測量結果 #OK
    if request.method == "POST":
        uid = request.user.id
        data = request.body
        data = str(data,encoding="utf-8").replace("%20"," ")
        a = re.split("=|&",str(data))
        try:
            systolic = a[7]
            diastolic = a[1]
            pulse = a[3]
            recorded_at = a[5]
            recorded_at = recorded_at.replace("%3A",":")
            Blood_pressure.objects.create(uid = uid, systolic = systolic, diastolic = diastolic, pulse = pulse, recorded_at = recorded_at)
            message = {"status":"0"}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def body_weight(request):       # 上傳體重測量結果 #ok
    if request.method == "POST":
        uid = request.user.uid
        data = request.body
        data = str(data,encoding="utf-8").replace("%20"," ").replace("%3A",":")
        a = re.split("=|&",str(data))
        try:
            weight = a[7]
            body_fat = a[3]
            bmi = a[1]
            recorded_at = a[5]
            Weight.objects.create(uid = uid, weight = weight, body_fat = body_fat, bmi = bmi, recorded_at = recorded_at)
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def BloodSugar(request):    # 上傳血糖測量結果 #ok
    if request.method == "POST":
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="UTF-8").replace("%20"," ").replace("%3A",":")
        a = re.split("=|&",str(data))
        print(a)
        try:
            sugar = a[7]
            timeperiod = a[9]
            recorded_at = a[5]
            Blood_sugar.objects.create(uid = uid, sugar = sugar, timeperiod = timeperiod, recorded_at= recorded_at)
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def last_load(request):     # 最後上傳時間
    if request.method == "GET":
        uid = request.user.uid
        data = request.body
        data = str(data, encoding="UTF-8")
        upload = []
        try:
            if Blood_pressure.objects.get(uid = uid):
                latest1 = Blood_pressure.objects.get(uid = uid).latest('recorded_at')
                latest1 = str(latest1.recorded_at)
                upload.append({"Blood Pressure":latest1})
            if Weight.objects.filter(uid = uid):
                latest2 = Weight.objects.get(uid = uid).latest('recorded_at')
                latest2 = str(latest2.recorded_at)
                upload.append({"Weight":latest2})
            if Blood_sugar.objects.filter(uid = uid):
                latest3 = Blood_sugar.objects.get(uid = uid).latest('recorded_at')
                latest3 = str(latest3.recorded_at)
                upload.append({"Blood_sugar":latest3})
            if Diary_diet.objects.get(uid = uid):
                latest4 = Diary_diet.objects.get(uid = uid).latest('recorded_at')
                latest4 = str(latest4.recorded_at)
                upload.append({"Diary_diet":latest4})
            message = {"status":"0",
                        "last_upload":upload}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def records(request):       # 上一筆紀錄資訊!+刪除日記記錄
    uid = request.user.uid
    if request.method == "POST":
        data = request.body
        data = str(data, encoding='UTF-8')
        message = []
        try:
            if Blood_pressure.objects.filter(uid = uid):
                latest1 = Blood_pressure.objects.filter(uid = uid).latest('recorded_at')
                message1 = {
                    "Blood Pressure":{
                    "id":latest1.id,
                    "user_id":latest1.uid, 
                    "systolic":latest1.systolic, 
                    "diastolic":latest1.diastolic, 
                    "pulse":latest1.pulse, 
                    "recorded_at":str(latest1.recorded_at)}}
                message.append(message1)
            if Weight.objects.filter(uid = uid):
                latest2 = Weight.objects.filter(uid = uid).latest('recorded_at')
                message2 = {
                    "Weight":{
                    "id":latest2.id,
                    "user_id":latest2.uid,
                    "weight":latest2.weight, 
                    "body_fat":latest2.body_fat, 
                    "bmi":latest2.bmi, 
                    "recorded_at":str(latest2.recorded_at)}}
                message.append(message2)
            if Blood_sugar.objects.filter(uid = uid):
                latest3 = Blood_sugar.objects.filter(uid = uid).latest('recorded_at')
                message3 = {
                    "blood_sugar": {
                    "id" :latest3.id,
                    "user_id":latest3.uid,
                    "sugar":int(latest3.sugar), 
                    "timeperiod":int(latest3.timeperiod), 
                    "recorded_at":str(latest3.recorded_at)}}
                message.append(message3)
            if Diary_diet.objects.filter(uid = uid):
                latest4 = Diary_diet.objects.filter(uid = uid).latest('recorded_at')
                message4 = {
                    "diary_diet":{
                    "id":latest4.id,
                    "user_id":latest4.uid,
                    "sugar":int(latest4.sugar), 
                    "timeperiod":int(latest4.timeperiod), 
                    "recorded_at":str(latest4.recorded_at)}}
                message.append(message4)
            timeperiod_list = ['晨起', '早餐前', '早餐後', '午餐前', '午餐後', '晚餐前', '晚餐後', '睡前']
            diets = data['diets']
            diet = timeperiod_list[(int(diets)-1)%8]
            output = {"status":"0",
                        "message":message}
        except :
            output = {"status":"1"}
        return JsonResponse(output)
    if request.method == "DELETE":
        data = request.body
        data = str(data, encoding="UTF-8")
        try:
            if Blood_pressure.objects.filter(uid = uid):
                data_list = Blood_pressure.objects.filter(uid = uid)
                for data in data_list:
                    data.delete()
            if Weight.objects.filter(uid = uid):
                data_list = Weight.objects.filter(uid = uid)
                for data in data_list:
                    data.delete()
            if Blood_sugar.objects.filter(uid = uid):
                data_list = Blood_sugar.objects.filter(uid = uid)
                for data in data_list:
                    data.delete()
            if Diary_diet.objects.filter(uid = uid):
                data_list = Diary_diet.objects.filter(uid = uid)
                for data in data_list:
                    data.delete()
            message = {"status":"0"}
        except:
            message= {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def diary(request):     # 日記列表資料
    uid = request.user.id
    date = request.GET.get("date")
    diary = []
    if request.method == "GET":
        try:
            if date:
                if Blood_pressure.objects.filter(uid = uid, date = date):
                    blood_pressures = Blood_pressure.objects.filter(uid = uid, date = date)
                    for blood_pressure in blood_pressures:
                        d1 = {
                        "id":blood_pressure.id,
                        "user_id":blood_pressure.uid, 
                        "systolic":blood_pressure.systolic,
                        "diastolic":blood_pressure.diastolic,
                        "pulse":blood_pressure.pulse,
                        "recorded_at":str(blood_pressure.recorded_at),
                        "type":"blood_pressure"
                        }
                        diary.append(d1)
                if Weight.objects.filter(uid = uid, date = date):
                    weights = Weight.objects.filter(uid = uid, date = date)
                    for weight in weights:
                        d2 = {
                        "id":weight.id,
                        "user_id":weight.uid,
                        "weight":weight.weight,
                        "body_fat":weight.body_fat,
                        "bmi":weight.bmi,
                        "recorded_at":str(weight.recorded_at),
                        "type":"weight"
                        }
                        diary.append(d2)
                if Blood_sugar.objects.filter(uid = uid, date = date):
                    blood_sugars = Blood_sugar.objects.filter(uid = uid, date = date)
                    for blood_sugar in blood_sugars:
                        d3 = {
                        "id":blood_sugar.id,
                        "user_id":blood_sugar.uid, 
                        "sugar":int(blood_sugar.sugar), 
                        "timeperiod":int(blood_sugar.timeperiod), 
                        "recorded_at":str(blood_sugar.recorded_at),
                        "type":"blood_sugar"
                        }
                        diary.append(d3)
                if Diary_diet.objects.filter(uid=uid, date=date):
                    diary_diets = Diary_diet.objects.filter(uid=uid, date=date)
                    for diary_diet in diary_diets:
                        if UserCare.objects.filter(uid=uid, date=date):
                            reply = UserCare.objects.filter(member_id=0, date=date).latest('updated_at')
                            d4 = {
                            "id":diary_diet.id,
                            "user_id":diary_diet.uid, 
                            "description":diary_diet.description, 
                            "meal":int(diary_diet.meal), 
                            "tag":diary_diet.tag, 
                            "image":diary_diet.image_count,
                            "type":"diet",
                            "location":
                                {
                                    "lat":diary_diet.lat,
                                    "lng":diary_diet.lng
                                },
                            "recorded_at":str(diary_diet.recorded_at),
                            "reply":reply.message
                        }
                        else:
                            d4 = {
                                    "id":diary_diet.id,
                                    "user_id":diary_diet.uid, 
                                    "description":diary_diet.description, 
                                    "meal":int(diary_diet.meal), 
                                    "tag":diary_diet.tag, 
                                    "image":diary_diet.image_count,
                                    "type":"diet",
                                    "location":
                                        {
                                            "lat":diary_diet.lat,
                                            "lng":diary_diet.lng
                                        },
                                    "recorded_at":str(diary_diet.recorded_at),
                                }
                            diary.append(d4)
            message = {"status":"0",
                        "Diary":diary}
        except :
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def diary_diet(request):        # 飲食日記
    if request.method == "POST":
        uid = request.user.uid
        data = request.body
        data = str(data, encoding='UTF-8').replace("%20"," ").replace("%3A",":")
        a = re.split("=|&",str(data))
        try:
            de_1 = unquote(a[1],'UTF-8')
            description = de_1
            meal = a[9]
            tag = request.POST.getlist("tag[][]")
            image = a[3]
            lat = a[5]
            lng = a[7]
            recorded_at = a[11]
            Diary_diet.objects.create(uid = uid, description = description, meal = meal, tag = tag, image_count = image, 
                                                            lat= lat, lng = lng, recorded_at = recorded_at )
            message = {"status":"0"}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def care(request):      # 送出關懷諮詢!+獲取關懷諮詢
    uid = request.user.uid
    nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == "POST":
        data = request.body
        data = str(data, encoding="UTF-8")
        data = re.split("=|&",str(data))
        de_1 = unquote(data[1],'UTF-8')
        try:
            message = de_1
            recorded_at = nowtime
            friend_list = Friend_data.objects.get(uid=uid, status=1)
            UserCare.objects.create(uid=uid, member_id=friend_list.friend_type, reply_id=friend_list.relation_id, message=message, updated_at=recorded_at)
            message1 = {"status":"0"}
        except Exception as e:
            print(e)
            message1 = {"status":"1"}
        return JsonResponse(message1)
    if request.method == "GET":
        data = request.body
        data = str(data, encoding="UTF-8")
        try:
            usercares = UserCare.objects.filter(reply_id=uid)
            cares = []
            for cares in usercares:
                r = {
                        "id":cares.id,
                        "user_id":cares.uid,
                        "member_id":cares.member_id,
                        "reply_id":cares.reply_id,
                        "message":cares.message,
                        "created_at":str(cares.created_at),
                        "updated_at":str(cares.updated_at)
                    }
                cares.append(r)
            message1 = {"status":"0", "cares":cares}
        except:
            message1 = {"message":"1"}
        return JsonResponse(message1)