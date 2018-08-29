from django.shortcuts import render, HttpResponse
from .featurespack.captcha import captcha
from django.http import HttpResponseRedirect
from django.views.decorators import csrf
import simplejson
# Create your views here.
import io
from django.core.exceptions import ObjectDoesNotExist
from adminproject.models import Account
import os
import time
import re
import json
from django.forms.models import model_to_dict
from adminproject.models import Classify
from adminproject.models import Acticle
from .page import page


def check_login(func):

    def all_views_check_login(request, *args, **kwargs):

        if request.session.get("user_id"):
                return func(request, *args, **kwargs)
        else:
                return HttpResponseRedirect("/admin/login")
    return all_views_check_login


@csrf.csrf_exempt
def admin_login(request):

                if request.method == "POST":
                    print(request.body)
                    req_login_data = simplejson.loads(request.body)
                    admin_username = req_login_data['Admin_username']
                    admin_passwd = req_login_data['Admin_passwd']
                    Captcha_Code = req_login_data['C_Code']

                    response_result = {"msg_status": 1000, "success": "", "error":""}  # 返回的结果
                    if Captcha_Code != request.session['verity_code']:
                        response_result['error'] = "验证码错误"
                        response_result['msg_status'] = 1004  # 1004验证码错误状态码
                        return HttpResponse(simplejson.dumps(response_result))
                    else:
                            try:
                                is_filter = Account.objects.filter(username=admin_username, password=admin_passwd)

                                if is_filter:
                                    request.session['user'] = admin_username
                                    request.session['user_id'] = is_filter.values_list("id")[0][0]
                                    response_result['success'] = "登陆成功"
                                    response_result['url'] = "/admin/index"
                                    return HttpResponse(simplejson.dumps(response_result))
                                else:
                                    response_result['error'] = "用户名和密码错误"
                                    response_result['msg_status'] = 1001   # 1000错误状态码
                                    return HttpResponse(simplejson.dumps(response_result))
                            except ObjectDoesNotExist as oj:
                                    response_result['error'] = oj.args[0]
                                    response_result['msg_status'] = 1002  # 1001异常的错误状态码
                                    return HttpResponse(simplejson.dumps(response_result))

                return render(request, "login/login.html")


def instance_captcha(request):

    instanceCaptcha = captcha.Captcha()

    code = instanceCaptcha.image_point()

    setfont = instanceCaptcha.set_font()

    verifycode = instanceCaptcha.captcha_code()

    instanceCaptcha.set_captcha_text((20, 5), captcha_code=verifycode, fonts=setfont)

    request.session['verity_code'] = verifycode

    stream = io.BytesIO()

    # 将图片对象im保存到stream对象里
    instanceCaptcha.instanceImage.save(stream, "png")

    # stream.getvalue()图片二级制内容，再通过HttpResponse封装，返回给前端页面

    return HttpResponse(stream.getvalue())


def logout(request):

    del request.session['user_id']
    return HttpResponseRedirect("/admin/login")


@check_login
def index(request):

    return render(request, "Index/index.html")


@check_login
def public_header(request):

    return render(request, "public/public_header.html", {"user": request.session.get("user")})


@check_login
def public_left(request):

    return render(request, "public/public_left.html")


@check_login
def acticle_publish(request, classify_id=None, p_n=1):
    print(p_n)
    print(classify_id)
    all_data = Classify.objects.values()
    list_data = list(all_data)
    render_json = {
            "page_total_number": "",  # 总页数
            "next_index": p_n,   # 下一个页数
            "last_index": p_n,   # 上一个页数
            "current_page_number": p_n,  # 当前页数
            "acticle_list": "",  # 文章列表显示
            "show_range": (),  # 显示的页数列表
            "each_page": "",  # 显示每页几条记录
            "c_id": classify_id, #分类的id
            "classify_list": [],  # 分页的栏目
            "show_page_num": ""  # 显示的页数
        }
    c_id = Classify.objects.values("id").order_by("id")[0]['id']
    last_classify_name = Classify.objects.values("classify_name").order_by("-id")[0]['classify_name']
    classify_id = classify_id or c_id

    render_json['classify_list'] = list_data
    render_json['last_classify_name'] = last_classify_name
    print(classify_id)
    instance_Acticle = Acticle.objects.all().filter(c_id=classify_id)
    if not instance_Acticle:
        render_json['show_page_num'] = "0"
        render_json['page_total_number'] = "0"
        render_json['c_id'] = classify_id
        return render(request, "acticle/acticle_publish.html", render_json)
    else:

        instance_page = page.Page(instance_Acticle, 3, 5, p_n)

        page_total = instance_page.get_count()  # 分页总条数

        render_json['page_total_number'] = page_total
        print(page_total)
        render_json['next_index'] = instance_page.next_page()

        render_json['last_index'] = instance_page.last_page()

        render_json['acticle_list'] = instance_page.select_limit_number()

        render_json['each_page'] = len(instance_page.select_limit_number())

        render_json['show_range'] = instance_page.page_range(p_n)

        render_json['c_id'] = classify_id

        render_json['show_page_num'] = instance_page.num_pages()

        return render(request, "acticle/acticle_publish.html", render_json)


def acticle_publish_delete(request, d_id=None):
        print(request.META['HTTP_REFERER'])
        print(d_id)
        return_info_url = request.META['HTTP_REFERER']

        is_delete = Acticle.objects.filter(id=d_id).delete()
        print(is_delete)
        if is_delete:

            return HttpResponseRedirect(return_info_url)
        else:
            return HttpResponse("<script>alert('删除失败');</script>")


# 发布文章
@check_login
def acticle_push(request, modify_id=None):

    classify_data_info = {
        "classify_info": [],
        "modify_classify_name": "",
        "modify_title": "",
        "is_template_show": 1,
        "title_value": "",
        "file_value": "",
        "subject_thumbnail": "",
        "content": ""
    }

    if request.method == "POST":

                return HttpResponse(simplejson.dumps({
                    "error": "no post this method",
                    "msg": "not data"
                }))

    elif not modify_id:
                classify_data_info['modify_title'] = "发布文章"

                all_classify_info = Classify.objects.values()

                list_classify = list(all_classify_info)

                classify_data_info['classify_info'] = list_classify

                return render(request, "acticle/acticle_push.html", classify_data_info)

    else:
                classify_data_info['is_template_show'] = 0

                classify_data_info['modify_title'] = "修改文章"

                a_list = Acticle.objects.filter(id=modify_id).values("content", "title", "uploads_file", "c_id")

                classify_data_info['content'] = a_list[0]['content']

                classify_data_info['title_value'] = a_list[0]['title']

                classify_data_info['subject_thumbnail'] = "<img src='"+a_list[0]['uploads_file']+"' class='img'>"

                classify_data_info['file_value'] = a_list[0]['uploads_file']

                c_name = Classify.objects.filter(id=a_list[0]['c_id']).values("classify_name")

                classify_data_info['modify_classify_name'] = c_name[0]["classify_name"]

                return render(request, "acticle/acticle_push.html", classify_data_info)


# 修改文章
def update_acticle_content(request):
    pass

@check_login
def public_index(request):

    return render(request, "public/public_index.html")


@csrf.csrf_exempt
def add_classify(request):

        if request.method == "POST":

                classify_name = request.POST['first_column']

                isFindSameClassifyName = Classify.objects.filter(classify_name=classify_name)

                if isFindSameClassifyName:
                    return HttpResponse(simplejson.dumps({
                        "status": False,
                        "msg": "存在相同的分类"
                    }))
                else:
                    is_insert = Classify.objects.create(classify_name=classify_name)

                    if is_insert:
                        return HttpResponse(simplejson.dumps({
                            "status": True,
                            "msg": "分类添加成功"
                        }))
                    else:
                        return HttpResponse(simplejson.dumps({
                            "status": False,
                            "msg": "分类添加异常"
                        }))


@csrf.csrf_exempt
@check_login
def change_password(request):

    if request.method == "POST":
        get_password = simplejson.loads(request.body)
        new_pwd = get_password['change_pwd']
        is_update_pwd = Account.objects.filter(id=request.session.get("user_id")).update(password=new_pwd)

        if is_update_pwd:
            return HttpResponse(simplejson.dumps({
                "msg": "修改成功",
                "status": True

            }))
        else:
            return HttpResponse(simplejson.dumps({
                "msg": "修改失败",
                "status": False
            }))
    return render(request, "login/change_psw.html")


@csrf.csrf_exempt
def upload_img(request):

    if request.method == 'POST':
        acticle_subject = request.POST['subject']
        acticle_content = request.POST['editor_content']
        acticle_classify_id = request.POST['classify']
        is_match_subject = re.match("[^<>/]{5,}", acticle_subject)
        is_match_content = re.match(".{15,}", acticle_content)
        is_same_title = Acticle.objects.filter(title=acticle_subject)
        acticle_push_result = {
            "status": True,
            "successmsg": "",
            "errormsg": ""
        }
        if is_same_title:
            acticle_push_result['status'] = False
            acticle_push_result['errormsg'] = "存在相同的标题"
            return HttpResponse(simplejson.dumps(acticle_push_result))
        elif not is_match_subject:
            acticle_push_result['status'] = False
            acticle_push_result['errormsg'] = "不能含有'<>/'特殊符号,标题至少要5个字符以上"
            return HttpResponse(simplejson.dumps(acticle_push_result))
        elif not is_match_content:
            acticle_push_result['status'] = False
            acticle_push_result['errormsg'] = "文章内容至少要15个字符以上"
            return HttpResponse(simplejson.dumps(acticle_push_result))
        elif acticle_classify_id == "":
            acticle_push_result['status'] = False
            acticle_push_result['errormsg'] = "分类名称不能为空"
            return HttpResponse(simplejson.dumps(acticle_push_result))
        elif not request.FILES:
            acticle_push_result['status'] = False
            acticle_push_result['errormsg'] = "上传文件不能为空"
            return HttpResponse(simplejson.dumps(acticle_push_result))
        else:
            try:
                file_path = handle_uploaded_file(request.FILES['file'])
                date_time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(date_time_now)
                is_create = Acticle.objects.create(content=acticle_content, create_time=date_time_now,
                                                   title=acticle_subject, uploads_file=file_path,
                                                   c_id=acticle_classify_id)
                if is_create:
                    acticle_push_result['status'] = True
                    acticle_push_result['successmsg'] = "添加成功"
                    return HttpResponse(simplejson.dumps(acticle_push_result))
                else:
                    acticle_push_result['status'] = False
                    acticle_push_result['errormsg'] = "添加失败"
                    return HttpResponse(simplejson.dumps(acticle_push_result))
            except FileExistsError as e:
                    acticle_push_result['status'] = False
                    acticle_push_result['errormsg'] = e.args
                    return HttpResponse(simplejson.dumps(acticle_push_result))
    else:

        return HttpResponse("error")


def handle_uploaded_file(f):
    file_name = str(int(round(time.time() * 1000)))+".jpg"
    file_path = os.path.join(os.path.dirname(__file__), "uploads")
    with open(os.path.join(file_path,  file_name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return "/adminproject/uploads/"+file_name


