from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
import base64
from logs.models import Log
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from profiles.models import Profile


from django.contrib.auth import authenticate, login

from .utils import is_ajax, classify_face

def login_view(request):
    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    return redirect('login') 


""" def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to the login page
    else:
        return redirect('home')   # Redirect to the home page if not a POST request
 """

""" def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to the login page
    else:
        # Return a 405 Method Not Allowed response for GET requests
        return HttpResponseNotAllowed(['POST']) """

@login_required
def home_view(request):
    return render (request, 'main.html', {})
    


def find_user_view(request):
    # if able to find user

    if is_ajax(request):
        photo = request.POST.get('photo')
        _, str_img = photo.split(';base64')
        decoded_file = base64.b64decode(str_img)

        x= Log()
        x.photo = ContentFile(decoded_file, 'upload.png')
        x.save()

        res = classify_face(x.photo.path)
        user_exists = User.objects.filter(username=res).exists()
        if user_exists:
            user = User.objects.get(username=res)
            profile = Profile.objects.get(user=user)
            x.profile = profile
            x.save()


            login(request, user)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})
