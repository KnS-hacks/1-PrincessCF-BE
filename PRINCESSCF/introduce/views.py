from .serializers import MemberSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json
import urllib3
from typing import Dict
from json import loads
from django.conf import settings
from .models import *

http = urllib3.PoolManager()
INTRODUCE_DATABASE_ID = getattr(settings, 'INTRODUCE_DATABASE_ID',
                                'INTRODUCE_DATABASE_ID')
INTERNAL_INTEGRATION_TOKEN = getattr(settings, 'INTERNAL_INTEGRATION_TOKEN',
                                     'INTERNAL_INTEGRATION_TOKEN')
Notion = getattr(settings, 'NOTION_VERSION', 'NOTION_VERSION')
headers = {
    'Authorization': f'Bearer {INTERNAL_INTEGRATION_TOKEN}',
    'Notion-Version': Notion,
    "Content-Type": "application/json"
}


def load_notionAPI_introduce():
    url = f"https://api.notion.com/v1/databases/{INTRODUCE_DATABASE_ID}/query"
    filter = {  # 가져올 데이터 필터
        "or": [{
            "property": "이름",
            "text": {
                "is_not_empty": True
            }
        }]
    }
    sorts = [  # 정렬
        {
            "property": "이름",
            "direction": "descending"
        }
    ]
    body = {"filter": filter, "sorts": sorts}
    response = http.request(
        'POST',
        url,
        body=json.dumps(body),  # json파일로 인코딩
        headers=headers,
        retries=False)
    source: Dict = loads(response.data.decode('utf-8'))  # 자료형 명시
    data = []
    for r in source['results']:
        name = r['properties']['이름']['title'][0]['plain_text']
        team = r['properties']['팀']['select']['name']
        participate = ([
            l['name'] for l in r['properties']['참여기수']['multi_select']
        ]) if '참여기수' in r['properties'] else None
        school = r['properties']['학교']['select']['name']
        try:
            introduce = r['properties']['소개']['rich_text'][0]['text'][
                'content']
        except:
            introduce = None
        interest = ([
            l['name'] for l in r['properties']['관심분야']['multi_select']
        ]) if '관심분야' in r['properties'] else None
        hashtag = ([
            l['name'] for l in r['properties']['\x08해쉬태그']['multi_select']
        ]) if '\x08해쉬태그' in r['properties'] else None
        data.append({
            'name': name,
            'team': team,
            'school': school,
            'introduce': introduce,
            'interest': interest,
            'hashtag': hashtag,
            'participate': participate,
        })
    return {'statusCode': 200, 'body': data}


def set_data():
    data = load_notionAPI_introduce()['body']
    t = []
    e = []
    m = []
    temp = []
    # Data Update or Create
    for d in data:
        i, created = Member.objects.update_or_create(name=d['name'])
        i.team = d['team']
        i.school = d['school']
        i.introduce = d['introduce']
        # interest
        if d['interest']:
            for inte in d['interest']:
                obj, c = Interest.objects.get_or_create(name=inte)
                i.interest.add(obj)
                e.append(inte)
        # hashtag
        if d['hashtag']:
            for hash in d['hashtag']:
                obj, c = HashTag.objects.get_or_create(name=hash)
                i.hashtag.add(obj)
                m.append(hash)
        # participate
        if d['participate']:
            for p in d['participate']:
                obj, c = Participate.objects.get_or_create(name=p)
                i.participate.add(obj)
                temp.append(p)
        i.save()
        t.append(d['name'])

    # Data Delete
    for db in Member.objects.all():
        if not db.name in t:
            Member.objects.get(name=db.name).delete()
    for db in Interest.objects.all():
        if not db.name in e:
            Interest.objects.get(name=db.name).delete()
    for db in HashTag.objects.all():
        if not db.name in m:
            HashTag.objects.get(name=db.name).delete()
    for db in Participate.objects.all():
        if not db.name in temp:
            Participate.objects.get(name=db.name).delete()


def introduce(request):
    set_data()
    introduce = Member.objects.all()
    return render(request, "introduce.html", {'introduce': introduce})


@csrf_exempt
def member_list(request):
    if request.method == 'GET':
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return JsonResponse(serializer.data, safe=False)


# @csrf_exempt
# def member_detail(request, name):
#     try:
#         member = Member.objects.get(name=name)
#     except Member.DoesNotExist:
#         return HttpResponse(status=404)
#     if request.method == 'GET':
#         serializer = MemberSerializer(member)
#         return JsonResponse(serializer.data)


@csrf_exempt
def team_member(request, team):
    try:
        member = Member.objects.filter(team=team)
    except Member.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MemberSerializer(member, many=True)
        return JsonResponse(serializer.data, safe=False)
