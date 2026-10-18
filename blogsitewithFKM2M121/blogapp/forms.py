from django.forms import ModelForm,Form
from django import forms 
from .models import blog,comment,bloguser,Tag
from django.forms.widgets import ClearableFileInput
from . import images, richtext


class blogform(ModelForm):
    class Meta:
        model=blog
        fields=['title','cover','content','genre']
        labels={'title':'Title: ','content':'','genre':'Genre: '}
    title=forms.CharField(label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''})
    )
    content=forms.CharField(label='',max_length=200_000,
        widget=forms.Textarea(attrs={'class':'form-control','placeholder': 'start your blog . . .','rows':'16'})
    )
    genre=forms.CharField(label='',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''})
    )
    tags=forms.CharField(label='',required=False,
        help_text=f'Comma separated, up to {Tag.MAX_PER_POST}.',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'django, orm, testing'})
    )

    cover=forms.ImageField(label='',required=False,
        widget=ClearableFileInput(attrs={'class':'form-control','accept':'image/jpeg,image/png,image/webp,image/gif'})
    )

    def clean_cover(self):
        cover = self.cleaned_data['cover']
        if cover and hasattr(cover, 'content_type'):  # a new upload, not the existing file
            return images.process(cover)
        return cover

    def clean_content(self):
        clean = richtext.clean_html(self.cleaned_data['content'])
        length = len(richtext.plain_text(clean))
        if length < 3000:
            raise forms.ValidationError(f'A post needs at least 3000 characters (this one has {length}).')
        if length > 10000:
            raise forms.ValidationError(f'A post can have at most 10000 characters (this one has {length}).')
        return clean

    def clean_tags(self):
        names = Tag.parse(self.cleaned_data['tags'])
        if len(names) > Tag.MAX_PER_POST:
            raise forms.ValidationError(f'Use at most {Tag.MAX_PER_POST} tags.')
        return names


class commentform(ModelForm):
    class Meta:
        model=comment
        fields=['comment_content']
        labels={'comment_content':''}
    comment_content = forms.CharField(label='',
        widget=forms.Textarea(attrs={'class':'form-control','rows': '5', 'cols': '50', 'placeholder': 'Enter your comment here'})
    )
    

class searchform(Form):
    search=forms.CharField(label='Search',required=True,min_length=3,max_length=100)


class userform(ModelForm):
    class  Meta:
        model=bloguser
        #optional fields:'date_of_birth','saves','posts','liked','comments','bio','status','date_of_joining','last_login','settings'
        fields=['first_name','last_name','email','mobile','password']
    first_name=forms.CharField(label='First Name',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'first_name'})
    )
    last_name=forms.CharField(label='Last Name',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'last_name'})
    )
    email=forms.EmailField(label='Email',
        widget=forms.TextInput(attrs={'class':'form-control','type':'email', 'placeholder':'email'})
    )
    mobile=forms.IntegerField(label='Mobile',
        widget=forms.TextInput(attrs={'class':'form-control','type':'number', 'placeholder':'number'})
    )
    
    password=forms.CharField(label='Password: ',required=True,widget=forms.TextInput(attrs={'class':'form-control','type':'password', 'placeholder':'Password'}))
    password2=forms.CharField(label='Password Confirmation',required=True,widget=forms.TextInput(attrs={'class':'form-control','type':'password', 'placeholder':'Password'}))
    
    

class edituserform(ModelForm):
    class  Meta:
        model=bloguser
        #fields=['user_name','dp','first_name','last_name','gender','date_of_birth','bio','instagram','facebook','linked_in','website','interests']
        
        fields=['user_name','dp','first_name','last_name','email','mobile','gender','date_of_birth','bio','instagram','facebook','linked_in','website','interests']
    user_name=forms.CharField(label='User Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    dp=forms.ImageField(label='Profile Pic',required=False,
        widget=ClearableFileInput(attrs={'class':'form-control'})
    )
    first_name=forms.CharField(label='First Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    last_name=forms.CharField(label='Last Name',
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    email=forms.EmailField(label='Email',required=False,
        widget=forms.TextInput(attrs={'class':'form-control','type':'email'})
    )
    mobile=forms.IntegerField(label='Mobile',required=False,
        widget=forms.TextInput(attrs={'class':'form-control','type':'number'})
    )
    gender=forms.ChoiceField(label='Gender',choices=bloguser.gchoices,
        widget=forms.RadioSelect(attrs={'class': 'form-check','type':'radio'})
    )
    relationship=forms.ChoiceField(label='Relationship Status',choices=bloguser.rchoices,
        widget=forms.Select(attrs={'class': 'form-select','type':'select'})
    )
    
    
    date_of_birth=forms.DateField(label='DOB',
        widget=forms.TextInput(attrs={'class':'form-control','type':'date'})
    )
    bio=forms.CharField(label='Bio',required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    instagram=forms.CharField(label='Instagram',required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    facebook=forms.CharField(label='Facebook',required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    linked_in=forms.CharField(label='LinkedIn',required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    website=forms.CharField(label='Website',required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    interests=forms.CharField(label='Interests',required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    
class loginform(Form):
    email=forms.CharField(label='User Name: ',required=True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'email'}))
    password=forms.CharField(label='Password: ',required=True,widget=forms.TextInput(attrs={'class':'form-control','type':'password', 'placeholder':'Password'}))

   
class smartform(Form):
    name=forms.CharField(label='Name: ',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email=forms.CharField(label='Email: ',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    mobile=forms.CharField(label='Mobile: ',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    address=forms.CharField(label='Address: ',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    city=forms.CharField(label='City: ',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    pin=forms.CharField(label='Pin Code: ',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='Password: ',required=True,widget=forms.TextInput(attrs={'class':'form-control','type':'password', }))


  

