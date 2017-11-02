# 该文件为一系列和数据库的接口

from backend.models import *
from django.contrib.auth.models import User

# 前后端衔接用
from django.http import HttpResponse
import json

# 获取某学院课程列表
# REQUIRES: type(col_id) == <class 'int'> && lower_value <= col_id <= upper_value
# MODIFIES: None
# EFFECTS: 返回学院编号为col_id的学院的课程列表,返回类型为list

def college_course_list(col_id):
    result = Course.objects.filter(college_id=col_id).values_list("id", flat=True)
    return list(result)

def college_course_list_sender(request):
	if request.method == "POST":
		result = college_course_list(request.POST.get('college_id'))
		return HttpResponse(json.dumps({
		    "course_id_list" : result
		}))

# 通过某课程类别获取课程列表
# REQUIRES: type(cla_id) == <class 'int'>
# MODIFIES: None
# EFFECTS: 返回某种课程类别的课程列表,返回类型为list

def classification_course_list(cla_id):
    result = Course.objects.filter(class_id=cla_id).values_list("id", flat=True)
    return list(result)

def classification_course_list_sender(request):
	if request.method == "POST":
		result = classification_course_list(request.POST.get('course_class'))
		return HttpResponse(json.dumps({
		    "course_id_list" : result
		}))

# 查询课程详细信息
# REQUIRES: type(cou_id) == <class 'int'>
# MODIFIES: None
# EFFECTS: 返回某个课程的所有信息,返回类型为dict,若课程不存在则返回空字典

def course_information(cou_id):
    result = Course.objects.filter(id=cou_id)
    if(len(result) == 0):
        return {}
    result = result.values()[0] 
    return result


def course_information_sender(request):
    if request.method == "POST":
    	result = course_information(request.POST.get('course_id'))
        if result == {}:
        	return HttpResponse(json.dumps({}))
        return HttpResponse(json.dumps({
            "name" : result.name,
            "hours" : result.hours,
            "credit" : result.credit,
            "teacher" : null,
            "college" : null, # College类需提供college_id属性
            "intro" : null,
            "picture" : null
        }))


# 查询课程贡献度列表
# REQUIRES: type(cou_id) == <class 'int'>
# MODIFIES: None
# EFFECTS: 返回某个课程的贡献度列表,表中元素为排好序的(user_id, score)元组,返回类型为list

def course_contribution_list(cou_id):
    temp = R_Course_User_Contribution.objects.filter(course_id=cou_id)
    if(len(temp) == 0):
        return []
    temp = temp.values_list("user_id", "score")
    keys = []
    for item in temp:
        if(item[0] not in keys):
            keys.append(item[0])
    values = []
    for key in keys:
        contrib = 0
        for item in temp:
            if(item[0] == key):
                contrib += item[1]
        values.append(contrib)
    
    result = list(zip(keys,values))
    result = sorted(result, key=lambda x:x[1], reverse=True)
    return result

def course_contribution_list_sender(request):
    if request.method == "POST":
    	result = course_contribution_list(request.POST.get('course_id'))
    	return HttpResponse(json.dumps({
    		"list" : result
    	}))

# 查询资源信息
# REQUIRES: type(resource_id) == <class 'int'>
# MODIFIES: None
# EFFECTS: 返回某个资源的所有信息,返回类型为dict,若资源不存在则返回空字典

def resource_information(resource_id):
    result = Resource.objects.filter(id=resource_id)
    if(len(result) == 0):
        return {}
    result = result.values()[0]
    return result

def resource_information_sender(request):
	if request.method == "POST":
		result = resource_information(request.POST.get('resource_id'))
		return HttpResponse(json.dumps({
			"name" : result.name,
			"size" : result.size,
		    "link" : result.link,
		    "intro" : result.intro,
		    "upload_time" : result.upload_time,
		    "upload_user_id" : result.upload_user_id,
		    "download_num" : null,
		    "like_num" : null,
		    "eva_pos_num" : null,
		    "eva_neg_num" : null
		}))

# 查询个人信息
# REQUIRES: type(username) == <class 'string'>
# MODIFIES: None
# EFFECTS: 返回某个用户的一些信息,返回类型为dict,若用户不存在则返回空字典

def user_information(username):
    result = User.object.filter(username=usernaem)
    if(len(result) == 0):
        return {}
    profile = User.objects.get(username=username).userprofile
    result = result.values('username', 'email')[0]
    result['nickname'] = profile.nickname
    result['gender'] = profile.gender
    result['intro'] = profile.intro
    return result