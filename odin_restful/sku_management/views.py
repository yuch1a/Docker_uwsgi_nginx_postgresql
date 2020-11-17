from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import SKU, Product


# Create your views here.
def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_skus=SKU.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_skus':num_skus, 'num_visits':num_visits},
    )

class ProductCreate(CreateView):
    model = Product
    fields = '__all__'
    #initial={'date_of_death':'05/01/2018',}

class ProductUpdate(UpdateView):
    model = Product
    fields = '__all__'

class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('products')

class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'product_list'

class SKUCreate(CreateView):
    model = SKU
    fields = '__all__'
    #initial={'date_of_death':'05/01/2018',}

class SKUUpdate(UpdateView):
    model = SKU
    fields = '__all__'

class SKUDelete(DeleteView):
    model = SKU
    success_url = reverse_lazy('skus')
class SKUListView(generic.ListView):
    model = SKU
    context_object_name = 'sku_list'

class SKUDetailView(generic.DetailView):
    model = SKU