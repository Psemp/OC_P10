from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm
from .models import Profile

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Merci {username}, votre compte a été créé avec succés, vous pouvez maintenant vous connecter')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def profile(request):
    user_pk = request.user.pk
    user_profile = Profile.objects.get(user_id=user_pk)
    products = user_profile.favorite.all()

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if p_form.is_valid:
            try:
                p_form.save()
                messages.success(request, 'Votre photo a été mise à jour !')
                return redirect('profile')
            except ValueError:
                messages.error(request, 'Veuillez mettre en ligne une image')
                return redirect('profile')

    else:
        p_form = ProfileUpdateForm()

    context = {
        "products": products,
        "p_form": p_form
    }
    return render(request, 'account/profile.html', context)
