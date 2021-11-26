import re

from django.core.checks import messages
from user.models import *
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import * 
from datetime import datetime
# Create your views here.

@csrf_exempt
def code(request):      # 獲取控糖團邀請碼
    if request.method == "GET":
        uid = request.user.uid
        data = request.body
        data = str(data,encoding='UTF-8')
        try:
            user_friend = Friend.objects.get(uid = uid)
            message = {"status":"0",
                        "invite_code":user_friend.invite_code}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def friend_list(request):   # 控糖團列表
    if request.method == "GET":
        uid = request.user.uid
        data = request.body
        data = str(data, encoding='UTF-8')
        try:
            if Friend_data.objects.filter(uid=uid, status=1):
                friends = []
                friends_list = Friend_data.objects.filter(uid=uid, status=1)
                for friend in friends_list:
                    user_pro = UserProfile.objects.get(id=4)
                    relation = UserSet.objects.get(uid=user_pro.uid)
                    created_at_userfile = datetime.strftime(relation.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(relation.updated_at, '%Y-%m-%d %H:%M:%S')
                    r = {
                            "id":user_pro.id,
                            "name":relation.name,
                            "account":relation.email,
                            "email":relation.email,
                            "phone":relation.phone,
                            "status":relation.status,
                            "group":relation.group,
                            "birthday":str(relation.birthday),
                            "height":relation.height,
                            "gender":relation.gender,
                            "verified":relation.verified,
                            "privacy_policy":relation.privacy_policy,
                            "must_change_password":relation.must_change_password,
                            "badge":int(relation.badge),
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile,
                            "relation_type":friend.friend_type
                        }
                    friends.append(r)
            message = {"status":"0", "friends":friends}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)

@csrf_exempt
def friend_send(request):       # 送出控糖團邀請
    if request.method == "POST":
        uid = request.user.uid
        time= datetime.now()
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S")
        data = request.body
        data = str(data, encoding='UTF-8')
        data = re.split("=|&",str(data))
        try:
            friend_type = data[3]
            invite_code = data[1]
            user_uid = Friend.objects.get(invite_code = invite_code)
            friend_uid = user_uid.id
        except Exception as e:
            print(e)
            message = {"status":"1"}  #邀請碼無效
        else:
            try:
                Friend_data.objects.get(uid=uid, relation_id=friend_uid, status = 1)
            except:
                try:
                    Friend_data.objects.create(uid=uid, relation_id=friend_uid, status=0, friend_type=friend_type, updated_at=nowtime)
                except Exception as e:
                    print(e)
                    message = {"status":"1"}
                else:
                    message = {"status":"0"}
            else:
                message = {"status":"2"}
        return JsonResponse(message)
@csrf_exempt
def friend_receive(request):        # 獲取控糖團邀請
    if request.method == "GET":
        data = request.body
        data = str(data, encoding="UTF-8")
        uid = request.user.id
        try:
            accept_list = Friend_data.objects.filter(relation_id =uid, status=0)
            accepts= []
            for accept_list_data in accept_list:
                user_pro = UserProfile.objects.get(uid=accept_list_data.uid)
                user = UserSet.objects.get(id=(user_pro.id-1))
                created_at_friendata = datetime.strftime(accept_list_data.created_at, '%Y-%m-%d %H:%M:%S')
                updated_at_friendata = datetime.strftime(accept_list_data.updated_at, '%Y-%m-%d %H:%M:%S')
                created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
                updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
                r = {
                    "id":accept_list_data.id,
                    "user_id":accept_list_data.uid,
                    "relation_id":accept_list_data.relation_id,
                    "type":accept_list_data.friend_type,
                    "status":accept_list_data.status,
                    "created_at":created_at_friendata,
                    "updated_at":updated_at_friendata,
                    "user":
                            {
                                "id":user.id,
                                "name":user.name,
                                "account":user.email,
                                "email":user.email,
                                "phone":user.phone,
                                "status":user.status,
                                "group":user.group,
                                "birthday":str(user.birthday),
                                "height":user.height,
                                "gender":user.gender,
                                "verified":user.verified,
                                "privacy_policy":user.privacy_policy,
                                "must_change_password":user.must_change_password,
                                "badge":int(user.badge),
                                "created_at":created_at_userfile,
                                "updated_at":updated_at_userfile
                            
                            }
                        }
                accepts.append(r)
            message = {"status":"0", "requests":accepts}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def friend_accept(request,friend_data_id):      # 接受控糖團邀請
    if request.method == "GET":
        data = request.body
        data = str(data, encoding="UTF-8")
        uid = request.user.uid
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            check = Friend_data.objects.get(id = friend_data_id, status = 0)
            Friend_data.objects.update(uid=uid, relation_id=check.id, status=1, read=True, imread=True, friend_type=check.friend_type, updated_at=nowtime)
            check.read = True
            check.status = 1
            check.updated_at = nowtime
            check.save()
            message = {"status":"0"}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def friend_refuse(request,friend_data_id):      # 拒絕控糖團邀請
    if request.method == "GET":
        data = request.body
        data = str(data, encoding="UTF-8")
        uid = request.user.id
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            check = Friend_data.objects.get(id = friend_data_id, status = 0)
            check.read = True
            check.status = 2
            check.updated_at = nowtime
            check.save()
            message = {"status":"0"}
        except:
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def friend_delete(request,friend_data_id):      # 刪除控糖團邀請
    if request.method == "GET":
        data = request.body
        data = str(data,encoding="UTF-8")
        uid = request.user.id
        try:
            Friend_data.objects.filter(uid = friend_data_id, status=1).delete()
            message = {"status":"0"}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)
@csrf_exempt
def friend_results(request): # 控糖團結果!
    uid = request.user.id
    if request.method == 'GET':
        if Friend_data.objects.filter(uid=uid, read=True, imread=False):
            results = []
            result = Friend_data.objects.filter(uid=uid, read=True, imread=False).latest('updated_at')
            user_pro = UserProfile.objects.get(id=result.relation_id)
            relation = UserSet.objects.get(uid=user_pro.uid)
            created_at_friendata = datetime.strftime(result.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_friendata = datetime.strftime(result.updated_at, '%Y-%m-%d %H:%M:%S')
            created_at_userfile = datetime.strftime(relation.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_userfile = datetime.strftime(relation.updated_at, '%Y-%m-%d %H:%M:%S')
            r = {
                "id":result.id,
                "user_id":result.uid,
                "relation_id":result.relation_id,
                "type":result.friend_type,
                "status":int(result.status),
                "read":result.read,
                "created_at":created_at_friendata,
                "updated_at":updated_at_friendata,
                "relation":
                        {
                            "id":user_pro.id,
                            "name":relation.name,
                            "account":relation.email,
                            "email":relation.email,
                            "phone":relation.phone,
                            "fb_id":user_pro.fb_id,
                            "status":relation.status,
                            "group":relation.group,
                            "birthday":str(relation.birthday),
                            "height":relation.height,
                            "gender":relation.gender,
                            "verified":relation.verified,
                            "privacy_policy":relation.privacy_policy,
                            "must_change_password":relation.must_change_password,
                            "badge":int(relation.badge),
                            "created_at":created_at_userfile,
                            "updated_at":updated_at_userfile
                        }
                    }
            result.imread = True
            result.save()
            results.append(r)
            output = {"status":"0", "results":results}
        else:
            output = {"status":"1"}
    return JsonResponse(output)
@csrf_exempt
def friend_remove(request):     # 刪除更多好友
    if request.method == 'DELETE':
        data = request.body
        data = str(data, encoding="UTF-8")
        uid = request.user.id
        try:
            ids_list = request.GET.getlist("ids")
            for ids in ids_list :
                Friend_data.objects.get(uid=ids, relation_id=uid, status=1).delete()
                Friend_data.objects.get(uid=uid, relation_id=ids, status=1).delete()
            message = {"status":"0"}
        except Exception as e:
            print(e)
            message = {"status":"1"}
        return JsonResponse(message)