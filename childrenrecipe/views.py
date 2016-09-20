#!/usr/bin/env Python
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from childrenrecipe.serializers import *
from .models import *
from .serializers import *
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated
)
from rest_framework.decorators import (
	api_view,
	permission_classes,
	parser_classes,
)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

# Create your views here.
class JSONResponse(HttpResponse):
        """
        An HttpResponse that renders its content into JSON.
        """
	def __init__(self, data, **kwargs):
        	content = JSONRenderer().render(data)
        	kwargs['content_type'] = 'application/json'
        	super(JSONResponse, self).__init__(content, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):

        queryset = Group.objects.all()
        serializer_class = GroupSerializer

class APIRootView(APIView):
    def get(self, request):
        year = now().year
        data = {

            'year-summary-url': reverse('year-summary', args=[year], request=request)
        }
        return Response(data)

class RecipeViewSet(viewsets.ModelViewSet):
	queryset = Recipe.objects.all()
	serializer_class = RecipeSerializer


#	def list(self, request):
#        	recipes = Recipe.objects.values('id', 'create_time', 'name', 'user', 'exihibitpic',\
#                   	              	         'introduce', 'tag__name', 'material__id',\
#                        	                 'material__name', 'material__quantity', 'material__measureunits',\
#                                	         'procedure__id', 'procedure__seq', 'procedure__describe',\
#                                        	 'procedure__image', 'tag__category_id__name')
#        	data = []
#		recipes = Paginator(recipes,10)
#	        page = request.GET.get('page',1)
#        	try:
#                	recipes = recipes.page(page)
#        	except PageNotAnInteger:
#                	recipes = recipes.page(1)
#        	except EmptyPage:
#                	recipes = recipes.page(recipes.num_pages)
#        	for recipe in recipes:
#            		tag_list = []
#            		tag_list.append({
#                    		'name': recipe['tag__name'],
#                    		'category_name': recipe['tag__category_id__name'],
#                    		})
#
#            		material_list = []
#            		material_list.append({
#                    		'id': recipe['material__id'],
#                    		'recipe_title': recipe['name'],
#                    		'name': recipe['material__name'],
#                    		'quatity': recipe['material__quantity'],
#                    		'measureunits': recipe['material__measureunits'],
#                    		})
#
#            		procedure_list = []
#            		procedure_list.append({
#                    		'id': recipe['procedure__id'],
#                    		'recipe': recipe['name'],
#                    		'seq': recipe['procedure__seq'],
#                    		'describe': recipe['procedure__describe'],
#                    		'image': recipe['procedure__image'],
#                    		})
#            		items = {
#                    		'tag': recipe['tag__name'],
#                    		'recipes': {
#                        	'id': recipe['id'],
#                        	'name': recipe['name'],
#                        	'user': recipe['user'],
#                        	'exihibitpic': recipe['exihibitpic'],
#                        	'introduce': recipe['introduce'],
#                        	'tag': tag_list,
#                        	'material': material_list,
#                        	'procedure': procedure_list,
#                        	},
#                    	}
#            		data.append(items)
#        		context =  {
#            	#		'status': status.HTTP_200_OK,
#            	#		'msg': 'OK',
#            			'data': data,
#            		}
#        	return Response(data,status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

class MaterialViewSet(viewsets.ModelViewSet):
	queryset = Material.objects.all()
	serializer_class = MaterialSerializer

class ProcedureViewSet(viewsets.ModelViewSet):
	queryset = Procedure.objects.all()
	serializer_class = ProcedureSerializer

class TagViewSet(viewsets.ModelViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def tags(request):
	data = []
	categorys = {}
	tags = Tag.objects.all()
	for tag in tags:
		tag_id = tag.id
		tag_name = tag.name
		category_name = tag.category.name
		categroy = None
		if category_name in categorys:
			category = categorys[category_name]
		else:
			category = {'category': category_name, 'tags': []}
			categorys[category_name] = category
			data.append(category)
		category['tags'].append({
			'id': tag_id,
			'tag': tag_name
		})
	return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def recipe(request):
        data = []
        tags = {}
        recipes = Recipe.objects.all()
        recipes = Paginator(recipes,10)
        page = request.GET.get('page',1)
        try:
                recipes = recipes.page(page)
        except PageNotAnInteger:
                recipes = recipes.page(1)
        except EmptyPage:
                recipes = recipes.page(recipes.num_pages)
        for recipe in recipes:
                recipe_id = recipe.id
                recipe_create_time = recipe.create_time
                recipe_name = recipe.name
                recipe_user = recipe.user
                recipe_exihibitpic = recipe.exihibitpic
                recipe_introduce = recipe.introduce
		recipe_tips = recipe.tips
	

                tag_name = recipe.tag.filter(category__is_tag= 1 )[0].name

                tag = None
                if tag_name in tags:
                        tag = tags[tag_name]
                else:
                        tag = {'tag':tag_name, 'recipes':[]}
                        tags[tag_name] = tag
                        data.append(tag)
                tag['recipes'].append({
                        'id':recipe_id,
			'url':"http://"+request.META['HTTP_HOST']+'/'+'api'+'/'+'recipes'+'/'+str(recipe_id),
                        'create_time':recipe_create_time,
                        'recipe':recipe_name,
                        'user':recipe_user,
			'tips':recipe_tips,
                        'exihibitpic':"http://"+request.META['HTTP_HOST']+recipe_exihibitpic.url,
                        'introduce':recipe_introduce,
                         'tag': [{"category_name": x.category.name, 'name': x.name}for x in recipe.tag.all()]
                })
        return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
def tagshow(request):
	data = []
        categorys = {}
        tags = Tag.objects.filter(category__is_tag= 1)
        for tag in tags:
                tag_id = tag.id
                tag_name = tag.name
                category_name = tag.category.name
                categroy = None
                if category_name in categorys:
                        category = categorys[category_name]
                else:
                        category = {'category': category_name, 'tags': []}
                        categorys[category_name] = category
                        data.append(category)
                category['tags'].append({
                        'id': tag_id,
                        'tag': tag_name
                })
        return Response(data, status=status.HTTP_200_OK)
