import requests.exceptions, requests
from .middleware import get_current_api_key,deactivate_key
from django.http import JsonResponse
import os
count=5

def searchNews(request):
    global count
    try:
        if request.method == 'GET':
            if(get_current_api_key() is False):
                return JsonResponse({"message":"No api key found"}, status=409)
            count+=1
            search = request.GET.get('q', '')
            api_url= "https://newsapi.org/v2/everything?q={}&apiKey={}".format(search,os.getenv('API_KEY'))
            try:
                response = requests.get(api_url)
                if response.status_code == 409 or count%10==0:
                    count=5
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