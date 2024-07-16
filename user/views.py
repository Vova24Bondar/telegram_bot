from pprint import pprint
from django.http import HttpResponse, JsonResponse
import json
import requests
from django.shortcuts import render
from user.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
TG_BASE_URL = 'https://api.telegram.org/bot'


# def hello_world(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             chat_id = data.get('message').get('chat').get('id')
#             response_data = {
#                 'chat_id': chat_id,
#                 'text': 'Hello, World!'
#             }
#             requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=response_data)
#             return JsonResponse({'message': 'ok'}, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#     else:
#         return HttpResponse("Hello world")
#
#
# def user_get(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             chat_id = data.get('message').get('chat').get('id')
#             user = get_object_or_404(User, pk=1)
#             username = user.username
#             first_name = user.first_name
#             last_name = user.last_name
#             password = user.password
#             response_data = {
#                 'chat_id': chat_id,
#                 'text': f'first_name: {first_name}, last_name: {last_name}, username: {username}, password: {password}'
#             }
#             requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=response_data)
#             return JsonResponse({'message': 'Message sent to Telegram'}, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#
#     return JsonResponse({'error': 'Method not allowed'}, status=405)

from django.shortcuts import redirect

# def login_required_custom(view_func):
#     def _wrapped_view(request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             data = json.loads(request.body)
#             chat_id = data.get('message').get('chat').get('id')
#             response_data = {
#             'chat_id': chat_id,
#             'text': f'You not authentificate'
#                  }
#             requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=response_data)
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view

def user_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        chat_id = data.get('message').get('chat').get('id')
        text = data.get('message').get('text')

        step = cache.get(f'{chat_id}_step', 1)

        if step == 1:
            response_data = {
                'chat_id': chat_id,
                'text': 'Please enter your first name.'
            }
            cache.set(f'{chat_id}_step', 2)
            requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=response_data)
            return JsonResponse({'message': 'First name requested successfully'}, status=200)

        elif step == 2:
            cache.set(f'{chat_id}_first_name', text)
            response_data = {
                'chat_id': chat_id,
                'text': 'Please enter your last name.'
            }
            cache.set(f'{chat_id}_step', 3)
            requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=response_data)
            return JsonResponse({'message': 'Last name requested successfully'}, status=200)

        elif step == 3:
            cache.set(f'{chat_id}_last_name', text)
            response_data = {
                'chat_id': chat_id,
                'text': 'Please enter your username.'
            }
            cache.set(f'{chat_id}_step', 4)
            requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=response_data)
            return JsonResponse({'message': 'Username requested successfully'}, status=200)

        elif step == 4:
            cache.set(f'{chat_id}_username', text)
            response_data = {
                'chat_id': chat_id,
                'text': 'Please enter your password.'
            }
            cache.set(f'{chat_id}_step', 5)
            requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=response_data)
            return JsonResponse({'message': 'Password requested successfully'}, status=200)

        elif step == 5:
            hashed_password = make_password(text)
            first_name = cache.get(f'{chat_id}_first_name')
            last_name = cache.get(f'{chat_id}_last_name')
            username = cache.get(f'{chat_id}_username')

            try:
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=hashed_password
                )

                response_data = {
                    'chat_id': chat_id,
                    'text': f'User successfully created. First name: {user.first_name}, Last name: {user.last_name}, Username: {user.username}, Hashed password: {user.password}'
                }
                requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=response_data)
                cache.delete_many(
                    [f'{chat_id}_first_name', f'{chat_id}_last_name', f'{chat_id}_username', f'{chat_id}_step'])
                return JsonResponse({'message': 'User created successfully'}, status=201)

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=400)