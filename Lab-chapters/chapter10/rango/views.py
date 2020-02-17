from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
# reverse()--look up URL names in the file <url.py>
from django.urls import reverse
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

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

    # Call the helper function to handle the cookies
    visitor_cookie_handler(request)

    response = render(request, 'rango/index.html', context=context_dict)

    # Return response back to the user, updating any cookies that need changed.
    return response


def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
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

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # When valid->save the new category to database
        # Confirm it by 'commit=True'
        # Redirect->back to the index view.
        if form.is_valid():
            # form.save(commit=True)
            # Give a reference to an instance of the created Category object
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
     try:
            category = Category.objects.get(slug=category_name_slug)
     except Category.DoesNotExist:
            category = None

     if category is None:
            return redirect(reverse('rango:index'))

     form = PageForm()

     if request.method == 'POST':
            form = PageForm(request.POST)
            if form.is_valid():
                    if category:
                           page = form.save(commit=False)
                           page.category = category
                           page.view = 0
                           page.save()
                           return redirect(reverse('rango:show_category', 
                                                                   kwargs={'category_name_slug':category_name_slug}))

            else:
                    print(form.errors)


     context_dict = {'form' : form, 'category': category}
     return render(request, 'rango/add_page.html', context=context_dict) 

def register(request):
    #  A boolean value 
    #  whether the registeration was secessful
    #  true when registration succeeds
    registered = False

    # If a HTTP POST->process form data
    if request.method == 'POST':
        #  Attempt to grab information from the raw form information
        #  Make use of UserForm and UserProfileForm 
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # if two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save the user's form data to the database
            user = user_form.save()

            # Now we hash the password with the set_password method
            # Once hashed, we can update the user object
            user.set_password(user.password)
            user.save()

            # Now sort the UserProfile instance
            # Set commit=False. This delays saving the model
            # Until we are ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Save the UserProfile model instance
            profile.save()

            # Update the variable and registeration was successful
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instance
        # These forms will be blank, reandy for user input
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # Gather the username and password provided by the user. 
        # This information is obtained from the login form. 
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>']
        # because the # request.POST.get('<variable>') returns None if the value does not exist, 
        # while request.POST['<variable>'] # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

# If we have a User object, the details are correct. 
# If None (Python's way of representing the absence of a value), 
# no user with matching credentials was found.
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    # back to the homepage
    return redirect(reverse('rango:index'))


# A helper method
def get_server_side_cookie(request, cookie, defalut_val=None):
       val = request.session.get(cookie)
       if not val:
              val = defalut_val
       return val

# Update the function definition
def visitor_cookie_handler(request):
       # Get the number of visits to this site
       # The COOKIES.get() function is to obtain the visits cookie
       # If the cookie exists, the value returned is casted to an integer
       # If the cookie doesn't exist, then the default value of 1 is used
       visits = int(get_server_side_cookie(request, 'visits', '1'))

       last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
       last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

       # If it is been more than a day since the last visit..
       if (datetime.now() - last_visit_time).days > 0:
              visits = visits + 1
              #update the last visit cookie now that we have updated the count
              request.session['last_visit'] = str(datetime.now())
       else:
              # Set the last visit cookie
              request.session['last_visit'] = last_visit_cookie

       # Update/Set the visits cookie
       request.session['visits'] = visits  
