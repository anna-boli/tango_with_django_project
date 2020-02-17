from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
      name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
      # Set the field to zero by default
      # Fields are hidden that users cannot enter a value.
      views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
      likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
      slug = forms.CharField(widget=forms.HiddenInput(), required=False)

      # An inline class to provide additional information on the form
      # Meta class to specify which fields we wish to include in the form through the fields tuple.
      class Meta:
           # Provide an association between the ModelForm and a model
           model = Category
           fields = ('name',)

class PageForm(forms.ModelForm):
      title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
      url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter the URL of the page.")
      views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
     
      class Meta:
           model = Page
           exclude = ('category',)

      def clean(self):
           cleaned_data = self.cleaned_data
        # get() method to obtain the form's values
        # here, get() method would return None rather thab raise a KeyError exception   
           url = cleaned_data.get('url')
        # If url is not empty but not start with 'http://',
        # then prepend 'http://'
           if url and not url.startswith('http://'):
                url = f'http://{url}'
                cleaned_data['url'] = url 
        # teturn the reference to the cleaned_data dictionary 
           return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)