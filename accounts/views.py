from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from orders.models import Order
from .forms import UserRegistrationForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.phone = request.POST.get('phone', '')
        request.user.gamer_tag = request.POST.get('gamer_tag', '')
        request.user.save()

        user_profile.bio = request.POST.get('bio', '')
        user_profile.favorite_platform = request.POST.get('favorite_platform', '')
        user_profile.save()

        return redirect('accounts:profile')

    context = {
        'orders': orders,
        'user_profile': user_profile,
    }
    return render(request, 'accounts/profile.html', context)