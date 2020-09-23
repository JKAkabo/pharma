from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, request
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, View, ListView, TemplateView, DetailView
from rest_framework import viewsets

from .models import GroupSale, Sale, Product, Stock, UserProfile
from .forms import AddToStockFormSet, AddSaleFormSet, AddBranchForm, AddProductFormSet, UserProfileForm
from .serializers import StockSerializer


# display image
upload_results = UserProfile.objects.get(pk=id)


@login_required
def list_group_sales(request):
    user = get_user(request)
    context = {'user': user}

    group_sales = GroupSale.objects.all()
    context = {
        'group_sales': group_sales,
        'image': upload_results,
    }
    return render(request, 'shelf/list_group_sales.html', context)


@login_required
def list_sales(request, group_sale_id):
    user = get_user(request)
    context = {'user': user}
    
    
    group_sale = get_object_or_404(GroupSale, id=group_sale_id)
    context = {
        'group_sale': group_sale,
        'image': upload_results,
    }
    return render(request, 'shelf/list_sales.html', context)


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
            context = {
                'formset': formset,
                'image': upload_results,
            }
            return render(request, 'shelf/add_sale.html', context)
    else:
        formset = AddSaleFormSet
        context = {
                'formset': formset,
                'image': upload_results,
                }
        return render(request, 'shelf/add_sale.html', context)


@login_required
def list_branches(request):
    user = get_user(request)
    context = {'user': user}

    branches = user.branch.pharmacy.branch_set.all()
    context = {
        'branches': branches,
        'image': upload_results,
            }
    return render(request, 'shelf/list_branches.html', context)




@login_required
def add_branch(request):
    user = get_user(request)
    context = {'user': user}

    if request.method == 'POST':
        form = AddBranchForm(data=request.POST)
        if form.is_valid():
            new_branch = form.save(commit=False)
            new_branch.pharmacy = user.branch.pharmacy
            new_branch.save()
            return redirect('shelf:list_branches')
    else:
        form = AddBranchForm
        context = {
            'form': form,
            'image': upload_results,
            }
        return render(request, 'shelf/add_branch.html', context)


@login_required
def group_sale_receipt(request, group_sale_id):
    user = get_user(request)
    context = {'user': user}

    group_sale = get_object_or_404(GroupSale, id=group_sale_id)
    #group_sale = GroupSale.objects.all()
    
    context = {
        'group_sale': group_sale,
        'image': upload_results,
            }

    return render(request, 'shelf/group_sale_receipt.html', context)


@login_required
def add_to_stock(request):
    user = get_user(request)
    context = {'user': user}

    if request.method == 'POST':
        formset = AddToStockFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                product = form.cleaned_data['product']
                units = form.cleaned_data['units']
                product.stock.units_left += units
                product.stock.save()
        else:
            context = {
                'formset': formset,
                'image': upload_results,
                }
            return render(request, 'shelf/add_to_stock.html', context)
    else:
        formset = AddToStockFormSet
        context = {
                'formset': formset,
                'image': upload_results,
                }
        return render(request, 'shelf/add_to_stock.html', context)


@login_required
def add_product(request):
    user = get_user(request)
    context = {'user': user}

    if request.method == 'POST':
        formset = AddProductFormSet(data=request.POST)
        if formset.is_valid():
            for form in formset:
                new_product = form.save(commit=False)
                new_product.branch = user.branch
                new_product.save()
            return redirect('shelf:list_products')
    else:
        formset = AddProductFormSet
        context = {
                'formset': formset,
                'image': upload_results,
                }
        return render(request, 'shelf/add_product.html', context)


@login_required
def list_products(request):
    user = get_user(request)
    context = {'user': user}

    
    products = Product.objects.filter(branch=user.branch)
    context = {
        'products': products,
        'image': upload_results,
        }  
    return render(request, 'shelf/list_products.html', context)

    



@method_decorator(login_required, name='dispatch')
class ListStocksView(ListView):
    template_name = 'shelf/list_stock.html'
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'user': get_user(self.request),
            'image': upload_results,
        }
        #context['user'] = get_user(self.request)
        return context


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    

# upload(post) image
class upload_avatar(TemplateView):

    form = UserProfileForm
    template_name = 'shelf/avatar.html'

    def post(self, request, *args, **kwargs):

        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            upload_submit = UserProfile(avatar = form.cleaned_data['avatar'])
            upload_submit.save() 
            return redirect('accounts:login')

            

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)        
