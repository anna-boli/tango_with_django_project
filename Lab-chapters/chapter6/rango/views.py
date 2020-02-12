from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

# Query the database for a list of ALL categories currently stored.
# Order the categories by the number of likes in descending order.
# Retrieve the top 5 only -- or all if less than 5
# Place the list in our context_dict dictionary(with our boldmessage!)
# that will be passed to the template engine.
# -likes:descending order.
# likes:ascending order.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict ={}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    
    context_dict = {'puttutorial': 'This tutorial has been put together by Bo Li.'}

    return render(request, 'rango/about.html', context = context_dict)
 

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine
    context_dict = {}
    # try:
    # the .get() method returns one model instance (if exist) or an exception
    # Retrieve all of the associated pages
    # The filter() method will returns a list of page objects or an empty list
    # Adds results list to the template context under name pages
    # Adds category objects from the database to the context dictionary to verify that the category exists
    # except:
    # If we didn't find the specified category, the template will display the "no category" message for us.
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None


    return render(request, 'rango/category.html', context=context_dict)

