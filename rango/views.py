from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm


def index(request):
    context = RequestContext(request)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list}
    for category in category_list:
        category.url = category.name.replace(' ','_')
    return render_to_response('rango/index.html',context_dict,context)

def about(request):
    context = RequestContext(request)
    context_dict = {'aboutmessage': "This is the about message"}
    return render_to_response('rango/about.html',context_dict,context)

def category(request, category_name_url):
    context = RequestContext(request)

    category_name = category_name_url.replace('_',' ')

    context_dict = {'category_name': category_name,
                    'category_name_url': category_name_url}

    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)

def add_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render_to_response('rango/add_category.html', {'form': form}, context)

def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = category_name_url.replace('_',' ')

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html', {}, context)

            page.views = 0
            page.save()

            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    return render_to_response('rango/add_page.html',
                              {'category_name_url': category_name_url,
                               'category_name': category_name, 'form': form},
                              context)