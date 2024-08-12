from .models import News
from dotenv import load_dotenv, set_key, find_dotenv
import os

load_dotenv(find_dotenv())
env_path = os.path.join(os.path.dirname(__file__), '../.env')

def activate_all_key():
    print("activating all keys")
    for key in News.objects.filter(isActive=False):
        key.isActive = True
        key.save()

def get_current_api_key():
    if os.getenv('API_KEY')=='':
        print("Changing api key")
        key = News.objects.filter(isActive=True).first()
        if key:
            set_key(env_path, 'API_KEY', key.key)
            os.environ['API_KEY'] = key.key
        else:
            activate_all_key()
            return False
        
def deactivate_key():
    new = News.objects.get(key=os.getenv('API_KEY'))
    new.isActive=False
    new.save()
    set_key(env_path, 'API_KEY', '')
    os.environ['API_KEY'] = ''