from django.conf import settings
from django.shortcuts import render
from gql import Client, gql
from graphene_django import settings as graphene_settings

from .query import get_query

val = getattr(settings, 'GRAPHENE', {})['SCHEMA']
schema = graphene_settings.perform_import(val, 'I dunno!')

graphqldoc_default_title = 'GraphQL API documentation'
graphqldoc_settings = getattr(settings, 'GRAPHQLDOC', {})
graphqldoc_title = graphqldoc_settings.get('TITLE', graphqldoc_default_title)
graphqldoc_logo = graphqldoc_settings.get('LOGO_URL', 'https://www.graphql.org/img/logo.svg')

client = Client(schema=schema)
query = gql(get_query(_type='general'))
result_schema = client.execute(query)

types = result_schema['__schema']['types']
query_type = result_schema['__schema']['queryType']
mutation_type = result_schema['__schema']['mutationType']

data = {}
for i in types:
    kind = i['kind']
    name = i['name']
    if data.get(kind):
        data[kind].append(name)
    else:
        data[kind] = [name]

context = {'gdoc_logo': graphqldoc_logo, 'gdoc_title': graphqldoc_title}

def index(request):
    context.update({
        'schema': result_schema['__schema'],
        'detail': result_schema['__schema']['queryType'],
        'sidemenu': sorted(data),
        'menu': data,
    })

    return render(request, 'index.html', context)

def detail(request, name):
    if name.upper() in data:
        sidemenu = data[name.upper()]
        context.update({
            'schema': result_schema['__schema'],
            'sidemenu': sorted(sidemenu),
            'menu': data,
        })
        return render(request, 'index.html', context)
    else:
        query = gql(get_query(name=name, _type='type'))
        result = client.execute(query)
        detail = result['__type']
        try:
            sidemenu = data[result['__type']['kind']]
        except TypeError:
            sidemenu = data['OBJECT']
        # caso seja um objeto
        query_fields = result_schema['__schema']['queryType']['fields']
        mutation_fields = result_schema['__schema']['mutationType']['fields']
        if not result['__type']:
            for field in query_fields:
                if name == field['name']:
                    detail = field
            if not detail:
                for field in mutation_fields:
                    if name == field['name']:
                        detail = field

    context.update({
        'schema': result_schema['__schema'],
        'detail': detail,
        'sidemenu': sorted(sidemenu),
        'menu': data,
    })
    return render(request, 'index.html', context)
