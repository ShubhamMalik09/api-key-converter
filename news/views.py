import requests.exceptions
from .models import News
from rest_framework.test import APIClient
from django.http import JsonResponse
import requests

api_key = ""
count=5

def activate_all_key():
    print("activating all keys")
    for key in News.objects.filter(isActive=False):
        key.isActive = True
        key.save()

def get_current_api_key():
    global api_key
    global count
    count+=1
    if api_key=="":
        print("Changing api key")
        key = News.objects.filter(isActive=True).first()
        if key:
            count=5
            api_key=key
        else:
            activate_all_key()
            return False
        
def deactivate_key():
    global api_key
    new = News.objects.get(key=api_key)
    new.isActive=False
    new.save()
    api_key=""

def searchNews(request):
    global count
    try:
        if request.method == 'GET':
            if(get_current_api_key() is False):
                return JsonResponse({"message":"No api key found"}, status=409)
            search = request.GET.get('q', '')
            api_url= "https://newsapi.org/v2/everything?q={}&apiKey={}".format(search,api_key)
            try:
                response = requests.get(api_url)
                if response.status_code == 409 or count%10==0:
                    deactivate_key()
                    searchNews(request)
                response.raise_for_status()
                return JsonResponse(response.json(), status=200)
                
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)