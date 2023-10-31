from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator,MaxLengthValidator,MinLengthValidator
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from blogapp.manager import UserManager


def validatedate(value):
    if value < date(1900, 1, 1) or value > date.today():
        raise ValidationError(
            ('Invalid birthdate'),
            code='invalid'
        )

class bloguser(AbstractUser):
    gchoices = [('M', 'Male'),('F', 'Female'),('O', 'Other')]
    rchoices=[('M', 'Married'),('U', 'Unmarried'),('D', 'Divorced'),('W', 'Widowed'),('I', 'In a Relationship'),('N', 'Not Interested')]
    
    username=None
    idu=models.CharField(null=True,max_length=10,default='ooo')
    #user_name=models.CharField(null=True,blank=True,unique=True,max_length=30,validators=[MinLengthValidator(3),MaxLengthValidator(30)])
    user_name=models.CharField(null=True,blank=True,max_length=30,validators=[MinLengthValidator(3),MaxLengthValidator(30)])
    first_name=models.CharField(null=True,blank=True,default='',max_length=30,validators=[MinLengthValidator(3),MaxLengthValidator(20)])
    last_name=models.CharField(null=True,blank=True,default='',max_length=30,validators=[MinLengthValidator(3),MaxLengthValidator(20)])
    email=models.EmailField(null=False,blank=False,unique=True,validators=[MinLengthValidator(8),MaxLengthValidator(50)])
    mobile=models.IntegerField(null=True,blank=True,validators=[MinValueValidator(6000000000),MaxValueValidator(9999999999)])
    gender=models.CharField(null=True,blank=True,default='M',max_length=1,choices=gchoices)
    date_of_birth=models.DateField(null=True,blank=True,validators=[validatedate])
    dp=models.ImageField(null=True,blank=True,upload_to='images/dp')
    relationship=models.CharField(null=True,blank=True,default='N',max_length=1,choices=rchoices)
    #password=models.CharField(max_length=20,null=False,validators=[MinLengthValidator(6),MaxLengthValidator(20)],blank=False)
    bio=models.CharField(max_length=500,validators=[MaxLengthValidator(300)],null=True)
    status=models.BooleanField(default=False,null=True)
    date_of_joining=models.DateField(null=True)
    last_login=models.DateTimeField(null=True)
    vip=models.BooleanField(blank=True,default=False)
    
    follows=models.ManyToManyField('self',related_name='followed_by',symmetrical=False,blank=True)
    saves=models.ManyToManyField('blog', related_name='saved_by',blank=True)
    instagram=models.CharField(null=True,blank=True,max_length=50,)
    facebook=models.CharField(null=True,blank=True,max_length=50,)
    linked_in=models.CharField(null=True,blank=True,max_length=50,)
    website=models.CharField(null=True,blank=True,max_length=50,)
    interests=models.CharField(null=True,blank=True,max_length=200,)
    settings=models.CharField(null=True,blank=True,max_length=1000)
    #posts=models.ManyToManyField(blog, related_name='author',blank=True)
    #liked=models.CharField(max_length=10,blank=True,null=True)
    #comments=models.ForeignKey(max_length=10,blank=True,null=True)
    #followers=models.CharField(max_length=10,blank=True,null=True)
    slug=models.SlugField(default='slugdefault',null=True,blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    object=UserManager()

class blog(models.Model):

    idb=models.CharField(max_length=10,default='ooo')
    title= models.CharField(max_length=50,null=False,validators=[MinLengthValidator(5),MaxLengthValidator(50)])
    content= models.TextField(null=False,validators=[MinLengthValidator(3000),MaxLengthValidator(10000)])
    author= models.ForeignKey(bloguser,on_delete=models.CASCADE)
    date_of_publish= models.DateTimeField()
    genre= models.CharField(max_length=30,null=False,validators=[MaxLengthValidator(20)])
    tags= models.CharField(max_length=200,null=False,validators=[MaxLengthValidator(50)])
    #image= models.ImageField()
    likes=models.IntegerField(validators=[MinValueValidator(0)])
    likeuser=models.TextField(default=',')
    likess=models.ManyToManyField('bloguser',related_name='blogs_like',blank=True)
    views=models.IntegerField(validators=[MinValueValidator(0)])
    #comments=models.ForeignKey(validators=[MinValueValidator(0)])
    slug=models.SlugField(default='slugdefault',null=False,blank=True)



class comment(models.Model):
    idc=models.CharField(max_length=10,default='ooo')
    #idu=models.CharField(max_length=10,default='ooo')
    idu=models.ForeignKey(bloguser,on_delete=models.CASCADE)
    idb=models.ForeignKey(blog,on_delete=models.CASCADE,blank=True)
    date_of_comment=models.DateField()
    comment_content=models.TextField(null=False,validators=[MinLengthValidator(1),MaxLengthValidator(100)],verbose_name="Com__ment",)
    #slug=models.SlugField(default='slugdefault',null=True,blank=True)


class smarttransaction(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    idc=models.CharField(blank=True,null=True,max_length=10,default='ooo')
    idu=models.CharField(blank=False,null=False,max_length=10)
    razor_pay_order_id=models.CharField(blank=True,null=True,max_length=50)
    razor_pay_payment_id=models.CharField(blank=True,null=True,max_length=50)
    razor_pay_payment_signature=models.CharField(blank=True,null=True,max_length=100)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    amount=models.FloatField(default=0.0,null=False)
    # transaction_st_tm=models.DateTimeField(default='2012-01-01 11:11:11',blank=False,null=False)
    transaction_dt_tm=models.DateTimeField(auto_now=True)
