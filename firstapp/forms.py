from django import forms
from .models import Message
from django.contrib.auth.models import User
import re
class Index_form(forms.Form):
    create_group = forms.CharField(max_length=40,required=False)
    status = forms.CharField(max_length=40,required=False)
    search_group = forms.CharField(max_length=40,required=False)
    def clean(self):
        total_data = super().clean()
        p1 = total_data['create_group']
        p2 = total_data['search_group']
        p3 = total_data['status']
        msg = Message.objects.all()
        groups_list = []
        for m in msg:
            groups_list.append(m.room_name)
        if p1 in groups_list:
            raise forms.ValidationError('This Group name already exist try another name')
        if p2 not in groups_list and p2 != "":
            raise forms.ValidationError('This group doesnt exist')
        if p3 not in ['Public','Private'] and p3 != "":
            raise forms.ValidationError('The status has to be either Public or Private')

class Signup(forms.ModelForm):
    username = forms.CharField(max_length=60)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    def clean(self):
        total_data = super().clean()
        username1 = total_data['username']
        first_name1 = total_data['first_name']
        last_name1 = total_data['last_name']
        p1 = re.fullmatch(r'[A-Za-z0-9]+', str(username1))
        p4 = re.fullmatch(r'[a-zA-Z]+', str(first_name1))
        p5 = re.fullmatch(r'[a-zA-Z]+', str(last_name1))
        if not p1:
            raise forms.ValidationError('No special characters in username')
        if not p4:
            raise forms.ValidationError('enter proper firstname, with no special characters and numbers')
        if not p5:
            raise forms.ValidationError('enter proper lastname, with no special characters and numbers')
    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name']

class Fg_username(forms.Form):
    username = forms.CharField(max_length=30)
    def clean(self):
        total_data = super().clean()
        p1 = total_data['username']
        msg = User.objects.filter(username=p1)
        if not len(msg) > 0 :
            raise forms.ValidationError("there is no user with this username, try again or Sign up again")

class Fg_confirm(forms.Form):
    new_password = forms.CharField(max_length=70)
    confirm_password = forms.CharField(max_length=70)
    def clean(self):
        total_data = super().clean()
        p1 = total_data['new_password']
        p2 = total_data['confirm_password']
        if p1 != p2:
            raise forms.ValidationError('Password Doesnt match')