from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .forms import blogform,commentform,loginform,userform,edituserform,loginform,userform,searchform,smartform
from .models import blog,comment,bloguser,smarttransaction
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
import razorpay
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt


def home(request):
    bt=blog.objects.all().order_by('-date_of_publish')[:3]
    bl=blog.objects.all().order_by('-likes')[:3]
    form=loginform()
    forms=searchform()
    return render(request, 'home.html',{'form':form,'forms':forms,'latestblog':bt,'popularblog':bl})


def userlogin(request):
    form=loginform()
    return render(request, 'userlogin.html',{'form':form})


def logindone(request):
    form=loginform(request.POST)
    if form.is_valid():
        fd=form.cleaned_data
        l=bloguser.objects.filter(email=fd['email'])
        if l.count() ==1:
            un=fd['email']
            ps=fd['password']
            print(un,ps)
            user=authenticate(email=un,password=ps )
            print(user)
            if user!=None:
                login(request,user)
                return redirect('/')
    form=loginform()
    return render(request, 'userlogin.html',{'form':form})

def logoutdone(request):
    logout(request)
    return redirect('/')


def newuser(request):
    form=userform()

    return render(request, 'newuser.html',{'form':form,'msg':''})

def dummy_users():
    fn= [
    "Emma", "Liam", "Olivia", "Noah", "Ava", "Isabella", "Sophia", "Mia", "Charlotte", "Amelia",
    "Harper", "Evelyn", "Abigail", "Emily", "Elizabeth", "Sofia", "Madison", "Avery", "Ella", "Scarlett",
    "Grace", "Chloe", "Victoria", "Riley", "Aria", "Lily", "Aubrey", "Zoey", "Penelope", "Lillian",
    "Addison", "Layla", "Natalie", "Camila", "Hannah", "Brooklyn", "Zoe", "Nora", "Leah", "Savannah",
    "Stella", "Elena", "Maya", "Hailey", "Aurora", "Addison", "Lucy", "Ellie", "Bella", "Paisley",
    "Hazel", "Natalie", "Luna", "Rylie", "Aurora", "Audrey", "Skylar", "Violet", "Zoey", "Bella",
    "Aurora", "Anna", "Nova", "Ellie", "Lucy", "Stella", "Ellie", "Addison", "Natalie", "Savannah",
    "Brooklyn", "Skylar", "Bella", "Savannah", "Ellie", "Lucy", "Addison", "Penelope", "Luna", "Skylar",
    "Zoey", "Addison", "Bella", "Ellie", "Scarlett", "Ellie", "Nora", "Aubrey", "Camila", "Stella",
    "Ellie", "Zoey", "Scarlett", "Lucy", "Anna", "Chloe", "Bella", "Addison", "Savannah", "Grace"]
    ln = [
    "Smith", "Johnson", "Brown", "Taylor", "Miller", "Anderson", "Williams", "Jones", "Clark", "White",
    "Adams", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Lewis", "Walker",
    "Hall", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams",
    "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell",
    "Parker", "Evans", "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook",
    "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward",
    "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price",
    "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long",
    "Patterson", "Hughes", "Flores", "Washington", "Butler", "Simmons", "Foster", "Gonzales", "Bryant", "Alexander",
    "Russell", "Griffin", "Diaz", "Hayes", "Myers", "Ford", "Hamilton", "Graham", "Sullivan", "Wallace"]
    from random import randint
    from datetime import datetime
    for j in range(100):
        i=randint(0,99)
        k=randint(0,99)
        u=bloguser.objects.all().order_by('-idu')[0]
        uid=str(int(u.idu)+1)
        mn=randint(6000000000,9999999999)
        d=f'{randint(1950,2022)}-{randint(1,12)}-{randint(1,28)}'
        dt=datetime.strptime(d,"%Y-%m-%d")
        gen = ['M','F','O']
        g=gen[randint(0,2)]
        ui=bloguser.objects.create(idu=uid,first_name=fn[i],last_name=ln[k],email=(fn[i]+str(randint(1,2000))+'@gmail.com'), \
											mobile=mn,gender=g,date_of_birth=dt,\
												date_of_joining=datetime.now().date())
        ui.set_password(fn[i]+'12345')
        ui.save()
    print('100 users created!')
def iduch():
    ul=bloguser.objects.filter(id__gt=11)
    for i in ul:
        i.idu=(i.id)-1
        i.save()
    print('save complete')


def followscript():
    ul=bloguser.objects.all().order_by('-idu')[1:]
    for i in ul:
        import random
        n=random.randint(25,75)
        nl= random.sample(range(1, 203 + 1), n)
        for j in nl:
            uj=bloguser.objects.get(idu=j)
            i.follows.add(uj)
    print('follow done')
    

def register(request):
    if request.method=='POST':
        form=userform(request.POST)
        if form.is_valid():
            fd=form.cleaned_data
            if fd['password']==fd['password2']:
                from datetime import datetime
                #uid=1
                u=bloguser.objects.all().order_by('-id')[0]
                #print([i.idu for i in u])
                uid=str(int(u.idu)+1)
                ui=bloguser.objects.create(idu=uid,first_name=fd['first_name'],last_name=fd['last_name'],email=fd['email'], \
                                           mobile=fd['mobile'],date_of_joining=datetime.now().date())                      
                ui.set_password(fd['password'])
                ui.save()
                
                return render(request, 'userlogin.html',{'form':form})
        return render(request, 'newuser.html',{'form':form,'msg':'Invalid details, check your fields and try again'})

    form=userform()
    return render(request, 'newuser.html',{'form':form,'msg':''})





def emailconfirmation(request,u):
    u1=bloguser.objects.get(idu=u)
    if request.method=='POST':

        fl=u1.follows.all()
        us=request.user
        if request.POST.get('otp')==request.POST.get('otpconf'):
            u1.status=True
            u1.save()
            msg='Congratulations! your email confirmation was successful . . '
            return render(request, 'user.html',{'u':u1,'msg':msg,'fl':fl,'us':us})
        msg='Sorry! your email confirmation Failed, Try again . . '
        return render(request, 'user.html',{'u':u1,'msg':msg,'fl':fl,'us':us})
    
    import random
    otp=str(random.randint(100000,999999))
    subject=f'Confirmation mail for Vblog account activaion for {u1.first_name} {u1.last_name}'
    message=f"This is you confirmation mail for your account activation. Please enter the OTP {otp} to confirm."
    from_email=settings.EMAIL_HOST_USER
    print(otp)
    recipient_list=[u1.email]
    send_mail(subject,message,from_email,recipient_list)
    return render(request, 'emailconfirmation.html',{'u':u,'otp':otp})



def smartblogupgrade(request,u):
    psu=bloguser.objects.get(idu=u)    
    formu=smartform()
    amount=1
    client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
    payment=client.order.create({'amount':amount*100,'currency':'INR','payment_capture':'0'})
    t1=smarttransaction.objects.create(idu=psu.idu,amount=amount,razor_pay_order_id=payment['id'],)
    t1.save()
    cb_url='http://'+ str(get_current_site(request))+"/smartblogsuccess/"
    return render(request, 'smartblogupgrade.html',{'u':u,'psu':psu,'formu':formu,'cb_url':cb_url,'k':settings.RAZORPAY_KEY_ID,'t1':t1,'payment':payment})

@csrf_exempt
def smartblogsuccess(request):
    context={}
    if request.method == "POST":
        order_id = request.POST.get('razorpay_order_id','')
        payment_id = request.POST.get('razorpay_payment_id', '')
        signature = request.POST.get('razorpay_signature','')
        resp_razorpay=dict(request.POST)
        t1=smarttransaction.objects.get(razor_pay_order_id=order_id) 
        u1=bloguser.objects.get(idu=t1.idu)
        t1.razor_pay_payment_id=payment_id
        t1.razor_pay_payment_signature=signature
        t1.save()

        params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
        client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
        result = client.utility.verify_payment_signature(params_dict)
        print(result)
        if result:
            t1.payment_status=1
            status=t1.get_payment_status_display()
            t1.save()
            u1.vip=True
            u1.save()

        context={"oid":t1.razor_pay_order_id,"pid":t1.razor_pay_payment_id,"psg":t1.razor_pay_payment_signature,
                 'status':status,'t1':t1,"su":u1}
        #print(context,resp_razorpay)
    return render(request, 'smartblogsuccess.html',context)
    

def blogview(request,b):
    u=request.user
    b1=blog.objects.get(idb=b)
    b1.views+=1
    b1.save()
    c1=comment.objects.filter(idb=b)
    cc=comment.objects.filter(idb=b).count()
    formc=commentform()
    
    return render(request,'blog.html',{'u':u,'b1':b1,'c1':c1,'cc':cc,'formc':formc})

@login_required(login_url='userlogin',)
def newblog(request):
    form=blogform()
    return render(request,'newblog.html',{'form':form})

@login_required(login_url='userlogin')
def createblog(request):
    from datetime import datetime
    form=blogform(request.POST)
    bl=blog.objects.all()
    l=1+len(bl)
    au=request.user
    if form.is_valid():
        f1=form.cleaned_data
        b1=blog(idb=l,title=f1['title'],content=f1['content'],genre=f1['genre'],
                tags=f1['tags'],author=au,date_of_publish=datetime.now(),likes=0,views=0)
        b1.save()
        b1=blog.objects.get(idb=l)
        c1=comment.objects.filter(idb=l)
        formc=commentform()
        return render(request,'blog.html',{'b1':b1,'c1':c1,'formc':formc})
    return render(request,'newblog.html',{'form':form})

@login_required(login_url='userlogin')
def like(request,b):
    b1=blog.objects.get(idb=b)
    u1=','+str(request.user.idu)+','
    if u1 not in b1.likeuser:
        b1.likeuser+=u1[1:]
        b1.likes+=1
    else:
        b1.likeuser=b1.likeuser.replace(u1,',')
        b1.likes-=1
    b1.save()
    return redirect('blog',b=b)
    

@login_required(login_url='userlogin')
def commentview(request,b):
    formc1=commentform(request.POST)
    if formc1.is_valid():
        bi=blog.objects.get(idb=b)
        cl=comment.objects.all()
        u1=bloguser.objects.get(idu=request.user.idu)
        l=1+len(cl)
        f2=formc1.cleaned_data
        from datetime import datetime
        c1=comment(idc=l,idu=u1,idb=bi,date_of_comment=datetime.now().date(),comment_content=f2['comment_content'])
        c1.save()
        return redirect('blog',b=b)

    return redirect('blog',b=b)

def genre(request,g):
    bl=blog.objects.filter(genre=g)
    l=len(bl)

    paginator = Paginator(bl, 3)
    page_number = request.GET.get('page')
    bpage = paginator.get_page(page_number)
    return render(request, 'bloglist.html',{'l':l,'t':g,'bl':bl,'bpage':bpage})

def latest(request):
    bl=blog.objects.all().order_by('-date_of_publish')
    l=len(bl)

    paginator = Paginator(bl, 3)
    page_number = request.GET.get('page')
    bpage = paginator.get_page(page_number)
    return render(request, 'bloglist.html',{'l':l,'t':'Latest','bl':bl,'bpage':bpage})

def popular(request):
    bl=blog.objects.all().order_by('-likes')
    l=len(bl)

    paginator = Paginator(bl, 3)
    page_number = request.GET.get('page')
    bpage = paginator.get_page(page_number)
    return render(request, 'bloglist.html',{'l':l,'t':'Popular','bl':bl,'bpage':bpage})

def tag(request):
    
    t=str(request.POST.get('search'))
    print(t)
    t1=t.replace(',', ' ')
    tl=t1.split(' ')
    bl=[]
    for i in tl:
        bli=blog.objects.filter(tags__icontains=i)
        bl+=list(bli)
    bl=set(bl)
    bl=list(bl)

    paginator = Paginator(bl, 3)
    page_number = request.GET.get('page')
    bpage = paginator.get_page(page_number)
    l=len(bl)
    return render(request, 'bloglist.html',{'l':l,'t':t,'bl':bl,'bpage':bpage})



def userprofile(request,u):
    u1=bloguser.objects.get(idu=u)
    fl=bloguser.object.filter(follows=u1)
    us=request.user
    
    return render(request, 'user.html',{'u':u1,'msg':'','fl':fl,'us':us})

def edituser(request,u):
    u1=bloguser.objects.get(idu=u)
    form=edituserform(instance=u1)
    return render(request, 'edituser.html',{'form':form,'msg':'','u':u})

        
def edituserdone(request,u):
        if request.method=='POST':
            form=edituserform(request.POST,request.FILES)
            
            print(form)
            if form.is_valid():
                fd=form.cleaned_data
                print(fd)
                u1=bloguser.objects.get(idu=u)
                print(u1.user_name,fd['user_name'])
                #'user_name','first_name','last_name','gender','date_of_birth','bio','social_media','interests',website
                if u1.user_name!=fd['user_name']:
                    u1.user_name=fd['user_name']
                print(fd)
                if fd['dp']:
                    u1.dp=fd['dp']
                u1.first_name=fd['first_name']
                u1.last_name=fd['last_name']
                u1.gender=fd['gender']
                u1.date_of_birth=fd['date_of_birth']
                u1.bio=fd['bio']
                u1.relationship=fd['relationship']
                u1.instagram=fd['instagram']
                u1.facebook=fd['facebook']
                u1.linked_in=fd['linked_in']
                u1.website=fd['website']
                u1.interests=fd['interests']
                u1.save()
                return render(request, 'user.html',{'u':u1,'msg':''})
        return render(request, 'edituser.html',{'form':form,'u':u,'msg':'Invalid details, check your fields and try again'})


def profilelist(request,lt):
    u1=request.user

    if lt=='fl':
        pl=u1.follows.all()
        plo=[]
        ttl='Subscriptions'
    elif lt=='fb':
        pl=u1.followed_by.all()
        plo=[]
        ttl= 'Subscribers'
    elif lt=='au':
        pl=bloguser.objects.all()
        plo=u1.follows.all()
        pl=list(set(pl)-set(plo))
        ttl='Blogers Not Subscribed'

    
    paginator = Paginator(pl, 20)
    page_number = request.GET.get('page')
    upage = paginator.get_page(page_number)
    return render(request, 'profilelist.html',{'pl':pl,'plo':plo,'ttl':ttl,'upage':upage,'msg':''})

def follow(request,f):
    u1=request.user
    f1=bloguser.objects.get(idu=f)
    u1.follows.add(f1)
    print('subscribed')
    return redirect(request.META.get("HTTP_REFERER"))

def unfollow(request,u):
    u1=request.user
    f1=bloguser.objects.get(idu=u)
    u1.follows.remove(f1)
    return redirect(request.META.get("HTTP_REFERER"))


