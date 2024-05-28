import requests
from tqdm import tqdm
import json

class VKClient:
    
    API_BASE_URL = 'https://api.vk.com/method/'
    
    def __init__(self, access_token):
        self.access_token = access_token

    def get_photos(self, user_id):
        param = {
            'access_token': self.access_token,
            'v': '5.236',
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1
        }
        response = requests.get(f'{self.API_BASE_URL}photos.get', params=param)
        return response.json()['response']['items']


class YandexDiskClient:

    API_BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, access_token):
        self.access_token = access_token

    def create_folder(self, folder_name):
        header = {'Authorization': f'OAuth {self.access_token}'}
        param = {'path': folder_name}
        response = requests.put(self.API_BASE_URL, headers=header, params=param)
        return response.json()

    def upload_photo(self, url, path):
        header = {'Authorization': f'OAuth {self.access_token}'}
        param = {
            'url': url,
            'path': path,
            'overwrite': 'true'
        }
        response = requests.post(f'{self.API_BASE_URL}/upload', headers=header, params=param)
        return response.json()
    


def func(vk_token, ya_token, vk_id):
    vk_client = VKClient(vk_token)
    ya_client = YandexDiskClient(ya_token)
    photos = vk_client.get_photos(vk_id)
    yadisk_foldername = 'VKPhotos'
    ya_client.create_folder(yadisk_foldername)

    uploaded_photos = []
    for photo in tqdm(photos[:5], desc='Загрузка фотографий'):
        max_size = max(photo['sizes'], key=lambda size: size['width'] * size['height'])
        photo_url = max_size['url']
        likes = photo['likes']['count']
        upload_date = photo['date']
        file_name = f'{likes}_{upload_date}.jpg'
        path = f'{yadisk_foldername}/{file_name}'
        ya_client.upload_photo(photo_url, path)
        uploaded_photos.append({'file_name': file_name, 'size': max_size['type']})

    with open('photos_info.json', 'w') as f:
        json.dump(uploaded_photos, f, indent=4)

    return f'Загружены фото на ЯДиск в папку {yadisk_foldername}'


print(func(vk_token = input('Введите ВК токен: '), ya_token = input('Введите ЯДиск токен: '), vk_id = input('Введите VKID: ')))








    



