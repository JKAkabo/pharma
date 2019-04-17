from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import BranchRegistrationForm, StaffRegistrationForm, StaffSignInForm, PharmacyRegistrationForm


def register_pharmacy(request):
    template_name = 'accounts/register_pharmacy.html'

    if request.method == 'POST':
        pharmacy_registration_form = PharmacyRegistrationForm(data=request.POST, prefix='pharmacy')
        branch_registration_form = BranchRegistrationForm(data=request.POST, prefix='branch')
        staff_registration_form = StaffRegistrationForm(data=request.POST, prefix='staff')
        if branch_registration_form.is_valid() and pharmacy_registration_form.is_valid() and staff_registration_form.is_valid():
            new_pharmacy = pharmacy_registration_form.save()

            new_branch = branch_registration_form.save(commit=False)
            new_branch.pharmacy = new_pharmacy
            new_branch.save()

            new_staff = staff_registration_form.save(commit=False)
            new_staff.branch = new_branch
            new_staff.save()

            pass
    else:
        context = {
            'branch_registration_form': BranchRegistrationForm(prefix='branch'),
            'pharmacy_registration_form': PharmacyRegistrationForm(prefix='pharmacy'),
            'staff_registration_form': StaffRegistrationForm(prefix='staff'),
        }
        return render(request, template_name, context)


def sign_in(request):
    template_name = 'accounts/sign_in.html'
    if request.method == 'POST':
        sign_in_form = StaffSignInForm(data=request.POST)
        if sign_in_form.is_valid():
            username = sign_in_form.cleaned_data['username']
            password = sign_in_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                pass
    else:
        context = {
            'sign_in_form': StaffSignInForm,
        }
        return render(request, template_name, context)


def sign_out(request):
    logout(request)
    return redirect('accounts:sign_in')
