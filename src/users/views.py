from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# pour ajouter un champ e-mail dans le formulaire, on a créé UserRegisterForm dans forms.py
# qui vient donc remplacer toutes les occurences de UserCreationForm, le formulaire de base
# ( donc on retire l'import from django.contrib.auth.forms import UserCreationForm)

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Votre compte a été créé ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')