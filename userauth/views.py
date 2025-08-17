from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .models import LikePost, Profile, Post
from userauth.models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    try:
        if request.method == 'POST':
            fnm = request.POST.get('fnm')
            emailid = request.POST.get('emailid')
            pwd = request.POST.get('pwd')
            my_user = User.objects.create_user(fnm,emailid,pwd)
            my_user.save()
            user_model = User.objects.get(username=fnm)
            new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
            new_profile.save()
            if my_user is not None:
                login(request, my_user)
                return redirect('/')
            return redirect('/login')
    except:
         invalid="User already exists"
         return render(request, 'signup.html',{'invalid':invalid})
  
    
    return render(request, 'signup.html')
                
def loginn(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        userr = authenticate(request,username=fnm,password=pwd)
        if userr is not None:
            auth_login(request, userr)
            return redirect('/')
        
            invalid="Invalid credentials"
            return render(request, 'loginn.html',{'invalid':invalid})
        
    return render(request, 'loginn.html')

@login_required(login_url='/loginn/')
def logoutt(request):
    logout(request)
    return redirect('/login')
            
            
@login_required(login_url='/loginn/')
def upload(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image_upload')
        caption = request.POST.get('caption')
        new_post = Post.objects.create(user=user.username, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/loginn/')    
def home(request):
    post=Post.objects.all().order_by('-created_at')
    #profile=Profile.objects.get(user=request.user)
    context={
        'post':post,
       # 'profile':profile
    }
    return render(request,'main.html',context)

@login_required(login_url='/loginn/')
def likes(request, id):
    if request.method == 'GET':
    
     username= request.user.username
     post=get_object_or_404(Post, id=id)
     
     like_filter=LikePost.objects.filter(post_id=id,username=username).first()
     if like_filter is None:
         new_like=LikePost.objects.create(post_id=id,username=username)
         post.no_of_likes += 1
     else:
         like_filter.delete()
         post.no_of_likes -= 1

         
    post.save()
    
    return redirect('/#'+id)

@login_required(login_url='/loginn/')
def home_posts(request, id):
    post = Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    
    context = {
        'post': post,
        'profile': profile
    }
    
    return render(request, 'main.html', context)





from userauth.models import Profile  # Make sure this import is at the top

@login_required(login_url='/loginn/')
def explore(request):
    post = Post.objects.all().order_by('-created_at')

    profile = None
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)

    context = {
        'post': post,
        'profile': profile,
    }

    return render(request, 'explore.html', context)

# def explore(request):
#     post = Post.objects.all().order_by('-created_at')
#     #profile = Profile.objects.get(user=request.user)
    
#     context = {
#         'post': post,
#         #'profile': profile
#     }
    
#     return render(request, 'explore.html', context)

@login_required(login_url='/loginn/')
def profile(request, username):  #id_user=username
    user_object = User.objects.get(username=username)
    profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object).order_by('-created_at')
    user_post_length = len(user_posts)
    
    # follower=request.user.username
    # user= user_object.username                  #user_id liya hai wo only
    # if Followers.objects.filter(follower=follower, user=user_object.username).first():
    #     follow_unfollow = 'Unfollow'
    # else:
    #     follow_unfollow = 'Follow'
    # user_followers=len(Followers.objects.filter(user=user_object.username))
    # user_following=len(Followers.objects.filter(follower=user_object.username))

    context = {
        'user_object': user_object,
        'profile': profile,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        # 'follow_unfollow': follow_unfollow,
        # 'user_following': user_following,
        # 'user_followers': user_followers,
    }

    if request.user.username == username:
        if request.method == 'POST':
            bio = request.POST.get('bio', '')
            location = request.POST.get('location', '')
            image = request.FILES.get('image')

            if image:
                user_profile.profileimg = image
            # Else image remains the same — no need to update

            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

            return redirect('/profile/' + username)
        else:
            return render(request, 'profile.html', context)

    return render(request, 'profile.html', context)


# def profile(request, id_user):
#     user_object=User.objects.get(username=id_user)
#     profile = Profile.objects.get(user=request.user)
#     user_profile= Profile.objects.get(user=user_object)
#     user_posts = Post.objects.filter(user=id_user).order_by('-created_at')
#     user_post_length=len(user_posts)
#     context = {
#         'user_object': user_object,
#         'profile': profile,
#         'user_profile': user_profile,
#         'user_posts': user_posts,
#         'user_post_length': user_post_length,
#     }
    
#     return render(request, 'profile.html', context)

# def follow(request):
#     if request.method == 'POST':
#         follower = request.POST['follower']
#         user= request.POST['user']
        
#         if Followers.objects.filter(follower=follower, user=user).first():
#          delete_follower= Followers.objects.get(follower=follower, user=user)
#          delete_follower.delete()
#          return redirect('/profile/'+user)
#         else:
#          new_follower = Followers.objects.create(follower=follower, user=user)
#          new_follower.save()
#          return redirect('/profile/'+user)
#     else:
#      return redirect('/')
        
@login_required(login_url='/loginn/')           
def delete(request, id):
    post= Post.objects.get(id=id)
    post.delete()
    return redirect('/profile/'+request.user.username)    

@login_required(login_url='/loginn/')
def search_results(request):
    query=request.GET.get('q')
    users=Profile.objects.filter(user__username__icontains=query)
    posts=Post.objects.filter(caption__icontains=query)
    context={
        'query': query,
        'users': users,
        'posts': posts
        
    }
    return render(request, 'search_user.html', context)
    
    
   