import form as form
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models.users import Profile, FollowRequest


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login! {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


#
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         uform = UserUpdateForm(request.POST, instance=request.user)
#         pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#
#         if uform.is_valid() and pform.is_valid():
#             uform.save()
#             pform.save()
#             messages.success(request, f'Account has been updated.')
#             return redirect('profile')
#     else:
#         uform = UserUpdateForm(instance=request.user)
#         pform = ProfileUpdateForm(instance=request.user.profile)
#
#     return render(request, 'users/profile.html', {'uform': uform, 'pform': pform})

# @login_required
# def profile(request, *args, **kwargs):
#     ids = request.user.id
#     user = User.objects.get(pk=ids)
#     if request.method == "POST":
#         if "bio" in request.POST and "user" in request.POST:
#             bio = request.POST["bio"]
#             location = request.POST["user"]
#
#             user.profile.bio = bio
#             user.profile.location = location
#             user.profile.save()
#
#     elif "image" in request.FILES:
#
#         image = request.FILES['image']
#         user.profile.Propic.save(image.name, image)
#
#     return render(request, 'users/profile.html', {"user": user})


@login_required()
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST,
                                  request.FILES,
                                  instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, f'Account has been updated.')
            return redirect('profile')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    # return redirect(reverse('profile', kwargs={'uform': uform, 'pform': pform}))

    return render(request, 'users/profile.html', {'uform': uform, 'pform': pform})


# @login_required
# def SearchView(request):
#     if request.method == 'POST':
#         kerko = request.POST.get('search')
#         print(kerko)
#         results = User.objects.filter(username__contains=kerko)
#         context = {
#             'results': results
#         }
#         return render(request, 'users/search_result.html', context)


@login_required
def SearchView(request):
    if request.method == 'POST':
        user_search = request.POST.get('search')
        print(user_search)
        results = User.objects.filter(username__startswith=user_search[:3])
        context = {
            'results': results
        }
        return render(request, 'users/search_result.html', context)


def friend_list(request):
    p = request.user.profile
    friends = p.friends.all()
    context = {
        'friends': friends
    }
    return render(request, "users/friend_list.html", context)



@login_required
def send_follow_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FollowRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    return HttpResponseRedirect('/users/{}'.format(user.profile.bio))