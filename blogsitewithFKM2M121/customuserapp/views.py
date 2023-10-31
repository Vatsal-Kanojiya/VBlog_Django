# from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
# from django.urls import reverse
# from .forms import loginform,userform,edituserform
# from .models import bloguser
# from django.contrib.auth import authenticate,login,logout,get_user_model
# from django.contrib.auth.decorators import login_required


# # Create your views here.


# def userlogin(request):
#     form=loginform()

#     return render(request, 'userlogin.html',{'form':form})


# def logindone(request):
#     form=loginform(request.POST)
#     if form.is_valid():
#         fd=form.cleaned_data
#         l=bloguser.objects.filter(email=fd['email'])
#         print('abc')
#         if l.count() ==1:
#             if l[0].password==fd['password']:
#                 return redirect('/')
#     form=loginform()
#     return render(request, 'userlogin.html',{'form':form})



# # def logindone(request):
# #     form=loginform(request.POST)
# #     if form.is_valid():
# #         fd=form.cleaned_data
# #         l=bloguser.objects.filter(email=fd['email'])
# #         if l.count() ==1:
# #             un=fd['email']
# #             ps=fd['password']
# #             print(un,ps)
# #             user=authenticate(email=un,password=ps )
# #             print(user)
# #             if user!=None:
# #                 return redirect('/')
# #     form=loginform()
# #     return render(request, 'userlogin.html',{'form':form})


# def newuser(request):
#     form=userform()

#     return render(request, 'newuser.html',{'form':form,'msg':''})

# def register(request):
#     if request.method=='POST':
#         form=userform(request.POST)
#         if form.is_valid():
#             fd=form.cleaned_data
#             if fd['password']==fd['password2']:
#                 from datetime import datetime
#                 u=bloguser.objects.all().order_by('-idu')[0]
#                 uid=str(int(u.idu)+1)
#                 #uid=1
#                 ui=bloguser.objects.create(idu=uid,email=fd['email'],mobile=fd['mobile'],password=fd['password'],\
#                     date_of_joining=datetime.now().date())                      
#                 ui.save()
#                 return render(request, 'userlogin.html',{'form':form})

#         return render(request, 'newuser.html',{'form':form,'msg':'Invalid details, check your fields and try again'})

#     form=userform()
#     return render(request, 'newuser.html',{'form':form,'msg':''})

# def userprofile(request,u):
#     u1=bloguser.objects.get(idu=u)
    
#     return render(request, 'user.html',{'u':u1,'msg':''})

# def edituser(request,u):
#     u1=bloguser.objects.get(idu=u)
#     form=edituserform(instance=u1)
#     return render(request, 'edituser.html',{'form':form,'msg':'','u':u})

        
# def edituserdone(request,u):
#         if request.method=='POST':
#             form=edituserform(request.POST,request.FILES)
#             print('a')
#             if form.is_valid():
#                 fd=form.cleaned_data
#                 u1=bloguser.objects.get(idu=u)
#                 print('b')
#                 #'user_name','first_name','last_name','gender','date_of_birth','bio','social_media','interests'
#                 u1.user_name=fd['user_name']
#                 u1.dp=fd['dp']
#                 u1.first_name=fd['first_name']
#                 u1.last_name=fd['last_name']
#                 u1.gender=fd['gender']
#                 u1.date_of_birth=fd['date_of_birth']
#                 u1.bio=fd['bio']
#                 u1.social_media=fd['social_media']
#                 u1.interests=fd['interests']
#                 u1.save()
#                 #print(u,u)
#                 return render(request, 'user.html',{'u':u1,'msg':''})
#         return render(request, 'edituser.html',{'form':form,'u':u,'msg':'Invalid details, check your fields and try again'})



# # def commentview(request,b):
# #     formc1=commentform(request.POST)
# #     if formc1.is_valid():
# #         bi=blog.objects.get(idb=b)
# #         cl=comment.objects.all()
# #         l=1+len(cl)
# #         f2=formc1.cleaned_data
# #         from datetime import datetime
# #         c1=comment(idc=l,idu='ooo',idb=b,date_of_comment=datetime.now().date(),comment_content=f2['comment_content'])
# #         c1.save()
# #         bi.comments+=1
# #         bi.save()
# #         return redirect('blog',b=b)

# #     return redirect('/')