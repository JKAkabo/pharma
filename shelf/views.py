from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import GroupSale
from .forms import AddSaleFormSet


@login_required
def add_sale(request):
    user = get_user(request)
    if request.method == 'POST':
        formset = AddSaleFormSet(data=request.POST)
        if formset.is_valid():
            group_sale = GroupSale.objects.create(attendant=user, sale_count=2)
            for form in formset:
                sale = form.save(commit=False)
                sale.group_sale = group_sale
                sale.save()
    else:
        formset = AddSaleFormSet
        context = {
            'user': user,
            'formset': formset
        }
        return render(request, 'shelf/add_sale.html', context)


@login_required
def list_branches(request):
    user = get_user(request)

    branches = user.branch.pharmacy.branch_set.all()
    context = {
        'user': user,
        'branches': branches,
    }
    return render(request, 'shelf/list_branches.html', context)
