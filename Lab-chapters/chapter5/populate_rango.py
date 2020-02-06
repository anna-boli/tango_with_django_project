import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')
import django
django.setup()
from rango.models import Category, Page

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    python_pages = [
        {'title': 'Official Python Tutorial',
         'url':'http://docs.python.org/3/tutorial/'},
        {'title': 'How to Think like a Computer Scientist',
         'url':'http://www.greenteapress.com/thinkpython/'},
        {'title': 'Learn Python in 10 Minutes',
         'url':'http://www.korokithakis.net/tutorials/python/'}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
        {'title': 'Django Rocks',
         'url':'http://www.djangorocks.com/'},
        {'title': 'How to Tango with Django',
         'url':'http://www.tangowithdjango.com/'}
    ]

    other_pages = [
        {'title': 'Bottle',
         'url':'http://bottlepy.org/docs/dev/'},
        {'title': 'Flask',
         'url':'http://flask.pocoo.org'}
    ]
# () tuples
# [] lists
# {} dictionary
    cats = {
        # 'Python':{'pages':python_pages},
        # 'Django':{'pages':django_pages},
        # 'Other Frameworks':{'pages':other_pages}
        ('Python',128,64):{'pages':python_pages},
        ('Django',64,32):{'pages':django_pages},
        ('Other Frameworks',32,16):{'pages':other_pages}
    }

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category
    # for loop to call the 'add_cat() & add_page()'functions repeatedly
    # c = add_cat(cat) because a 'Page' requires a 'Category' reference
    for cat, cat_data in cats.items():
        # c = add_cat(cat)
        c = add_cat(cat[0], cat[1], cat[2])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])
            

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

# get_or_create() returns a tuple of (object, created) 
# object is a reference to the model instance 
# that get_or_create() to check if the entry exists in the databse for us
# The entry is created using parameters you pass to the method 
# parameters: e.g. category,title,url,views
# created is a boolean value
# [0] returns the object reference only
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

# def add_cat(name):
def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    if c.name=='Python':
        c.views=128
        c.likes=64
    elif c.name=='Django':
        c.views=64
        c.likes=32
    elif c.name=='Other Frameworks':
        c.views=32
        c.likes=16
    c.save()
    return c


# Start execution here!
# populate() keeps tabs on categories that are created.
if __name__ =='__main__':
    print('Starting Rango population script...')
    populate()