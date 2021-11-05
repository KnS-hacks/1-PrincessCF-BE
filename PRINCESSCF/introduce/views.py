from django.shortcuts import render
import json
import urllib3
from typing import Dict
from json import loads
from django.conf import settings
from .models import Member

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
            "property": "Name",
            "text": {
                "is_not_empty": True
            }
        }]
    }
    sorts = [  # 정렬
        {
            "property": "Name",
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
        name = r['properties']['Name']['title'][0]['plain_text']
        team = r['properties']['Team']['select']['name']
        tag = ([l['name'] for l in r['properties']['Tag']['multi_select']
                ]) if 'Tag' in r['properties'] else 'None'
        data.append({
            'name': name,
            'team': team,
            'tag': tag,
        })
    return {'statusCode': 200, 'body': data}


def set_data():
    data = load_notionAPI_introduce()['body']
    temp = []
    # Data Update or Create
    for d in data:
        i, created = Member.objects.update_or_create(name=d['name'])
        i.team = d['team']
        i.tag = d['tag']
        i.save()
        temp.append(d['name'])

    # Data Delete
    for db in Member.objects.all():
        if not db.name in temp:
            Member.objects.get(name=db.name).delete()


def introduce(request):
    set_data()
    introduce = Member.objects.all()
    return render(request, "introduce.html", {'introduce': introduce})
