from django.contrib.auth import authenticate, login as lin, logout as lout
from django.shortcuts import render, redirect
from .forms import UserImageForm, BranchRegistrationForm, StaffRegistrationForm, StaffLoginForm, PharmacyRegistrationForm
from pharma.settings.base import AUTH_USER_MODEL

def register_pharmacy(request):
    if request.method == 'POST':
        agree = request.POST.get('agree', False)
        pharmacy_registration_form = PharmacyRegistrationForm(data=request.POST, prefix='pharmacy')
        branch_registration_form = BranchRegistrationForm(data=request.POST, prefix='branch')
        staff_registration_form = StaffRegistrationForm(data=request.POST, prefix='staff')
        #staff_picture_form = UserImageForm(data=request.POST, prefix='profile_pic')
        if agree and pharmacy_registration_form.is_valid() and branch_registration_form.is_valid() and staff_registration_form.is_valid():
            new_pharmacy = pharmacy_registration_form.save()

            new_branch = branch_registration_form.save(commit=False)
            new_branch.pharmacy = new_pharmacy
            new_branch.save()

            password = staff_registration_form.cleaned_data['password']
            new_staff = staff_registration_form.save(commit=False)
            new_staff.branch = new_branch
            new_staff.set_password(password)
            new_staff.save()

            #new_staff_picture = staff_picture_form.cleaned_data['profile_pic']
            #new_staff_picture.save()
#            staff_picture_form.save(commit=False)
            return redirect('accounts:login')
        else:
            context = {
                'branch_registration_form': branch_registration_form,
                'pharmacy_registration_form': pharmacy_registration_form,
                'staff_registration_form': staff_registration_form,
 #               'staff_picture_form': staff_picture_form,
            }
            return render(request, 'accounts/register_pharmacy.html', context)

    else:
        context = {
            'branch_registration_form': BranchRegistrationForm(prefix='branch'),
            'pharmacy_registration_form': PharmacyRegistrationForm(prefix='pharmacy'),
            'staff_registration_form': StaffRegistrationForm(prefix='staff'),
     #       'staff_picture_form': UserImageForm(prefix='picture'),
        }
        return render(request, 'accounts/register_pharmacy.html', context)


def login(request):
    if request.method == 'POST':
        login_form = StaffLoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                lin(request, user)
                return redirect('shelf:list_branches')
            else:
                login_form.add_error(field=None, error='Incorrect username or password')
                context = {
                    'login_form': login_form,
                }
                return render(request, 'accounts/login.html', context)
        else:
            return render(request, 'accounts/login.html', {'login_form': login_form})
    else:
        context = {
            'login_form': StaffLoginForm,
        }
        return render(request, 'accounts/login.html', context)


def logout(request):
    lout(request)
    return redirect('accounts:login')


def update_profile(request, user_id):
    user = AUTH_USER_MODEL.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()