from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import GroupSale
from .forms import AddSaleFormSet


@login_required
def add_sale(request):
    user = get_user(request)
    context = {'user': user}

    if request.method == 'POST':
        formset = AddSaleFormSet(data=request.POST)
        if formset.is_valid():
            sale_count = int(request.POST['form-TOTAL_FORMS'])
            group_sale = GroupSale.objects.create(attendant=user, sale_count=sale_count)
            for form in formset:
                sale = form.save(commit=False)
                sale.group_sale = group_sale
                sale.save()
            return redirect('shelf:group_sale_receipt', group_sale_id=group_sale.id)
        else:
            context['formset'] = formset
            return render(request, 'shelf/add_sale.html', context)
    else:
        formset = AddSaleFormSet
        context['formset'] = formset
        return render(request, 'shelf/add_sale.html', context)


@login_required
def list_branches(request):
    user = get_user(request)
    context = {'user': user}

    branches = user.branch.pharmacy.branch_set.all()
    context['branches'] = branches
    return render(request, 'shelf/list_branches.html', context)


@login_required
def group_sale_receipt(request, group_sale_id):
    user = get_user(request)
    context = {'user': user}
    group_sale = get_object_or_404(GroupSale, id=group_sale_id)
    context['group_sale'] = group_sale
    return render(request, 'shelf/group_sale_receipt.html', context)
