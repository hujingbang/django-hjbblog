from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from adminproject.models import Acticle,Classify
# Create your views here.


@csrf_exempt
def index(request):

        index_content = {
            "title_name": "胡经邦的博客",
            "show_acticle_list": "",
            "left_classify_list": ""
        }
        show_acticle_list = select_all_acticle()

        classify_list = Classify.objects.all().values()

        for item in classify_list:

            item['title_list'] = list(Acticle.objects.filter(c_id=item['id']).values("title","id","c_id"))

        for item in show_acticle_list:

            classify_once_name = list(Classify.objects.filter(id=item['c_id']).
                                      values("classify_name"))[0]['classify_name']

            item['classify_name'] = classify_once_name

        index_content['left_classify_list'] = classify_list
        index_content['show_acticle_list'] = show_acticle_list
        return render(request, "index.html", index_content)


@csrf_exempt
def details(request, id, c_id):
    get_c_name = Classify.objects.filter(id=c_id).values("classify_name")

    show_once_acticle = Acticle.objects.filter(id=id).values()

    if not show_once_acticle or not get_c_name:
        return render(request, "404.html")
    else:
        get_classify_name = get_c_name[0]["classify_name"]
        print(show_once_acticle)
        render_acticle_data = {
            "show_essay_list": show_once_acticle,
            "get_classify_name": get_classify_name,
            "acticle_content": show_once_acticle[0]['content']
        }
    return render(request, "details.html", render_acticle_data)


def select_all_acticle():
        acticle_list = Acticle.objects.all().values()

        return acticle_list






