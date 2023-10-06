from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import *
from django.contrib import messages
from .form import *
from .models import *
from django.contrib.auth.models import User





#yetkilendirme bölümü


def approve_user(request, user_id):
    if request.user.is_superuser:
        user_profile = get_object_or_404(SiteUser, user__username=user_id)
        user_profile.is_active = True
        user_profile.save()
    return render(request, 'index.html')  # Profil sayfanıza yönlendirme yapın

def grant_moderator(request, user_id):
    if request.user.is_superuser:  # Sadece admin yetkilisi bu işlemi yapabilir
        user_profile = get_object_or_404(SiteUser, user__username=user_id)
        user_profile.is_moderator = True
        user_profile.save()
        return redirect('admin_dashboard')  # Moderatör yetkisi verildikten sonra yönlendirilecek sayfa
    else:
        return HttpResponseForbidden("Bu işlemi yapmaya yetkiniz yok.")

def revoke_moderator(request, user_id):
    if request.user.is_superuser:  # Sadece admin yetkilisi bu işlemi yapabilir
        user_profile = get_object_or_404(SiteUser, user__username=user_id)
        user_profile.is_moderator = False  # Moderatör yetkisini kaldırın
        user_profile.save()
        return redirect('admin_dashboard')  # Moderatör yetkisi kaldırıldıktan sonra yönlendirilecek sayfa
    else:
        return HttpResponseForbidden("Bu işlemi yapmaya yetkiniz yok.")
    
def admin_dashboard(request):
    
    if request.user.is_superuser:
        reported_tweets = ReportedTweet.objects.all()
        reported_comments = ReportedComment.objects.all()
        users = User.objects.all()
        return render(request, 'admin-dashboard.html', {'users': users, 'reported_comments': reported_comments, 'reported_tweets': reported_tweets})
    else:
        return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")    

def ban_user(request, username):
    if request.user.is_staff:
        messages.success(request, f"{username} kullanıcısını yasaklama girişiminde bulunuluyor.")
        user_to_ban = get_object_or_404(User, username=username)
        
        if user_to_ban:
            BannedUser.objects.create(user=user_to_ban, reason="Uygunsuz davranış")
            user_to_ban.delete()

    return redirect('homepage')


def unban_user(request, username):
    if request.user.is_staff:
        # Kullanıcının engelini kaldırmak istediği kullanıcıyı al
        user_to_unban = get_object_or_404(User, username=username)
        
        if user_to_unban:
            # Var olan EngellenenKullanici girişini bul, eğer varsa sil
            banned_user_entry = BannedUser.objects.filter(user=user_to_unban).first()
            if banned_user_entry:
                banned_user_entry.delete()
            
            # Kullanıcının hesabını yeniden etkinleştir
            user_to_unban.is_active = True
            user_to_unban.save()
            
            messages.success(request, f'Kullanıcı {username} engeli kaldırıldı.')

    return redirect('homepage')

def report_tweet(request, tweet_id):
    try:
        tweet = Tweet.objects.get(id=tweet_id)
    except Tweet.DoesNotExist:
        return redirect('homepage')  # Tweet bulunmuyorsa Anasayfaya yönlendirir

    if request.method == 'POST':
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            # Form var ise veriyi işle
            reason = form.cleaned_data['content']
            reporter = request.user

            # Yeni bir RaporluTweet örneği oluşturun ve veritabanına kaydedin
            ReportedTweet.objects.create(  # 'tweet.user', tweet'i atan kullanıcıyı işaret ediyorsa
                reported_tweet=tweet,
                reporter=reporter,
                reason=reason
            )

           
            return redirect('homepage')  # 'homepage' yerine uygun URL ile değiştirin

    else:
        form = ReportCommentForm()

    # Formu template ile birlikte yükle
    return render(request, 'report_tweet.html', {'form': form, 'tweet_id': tweet_id})

def report_comment(request, comment_id):
    reported_comments = ReportedComment.objects.all()

    if request.method == 'POST':
        form = ReportCommentForm(request.POST)
        if form.is_valid():

            try:
                comment = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                return redirect('homepage')    
            # Form var ise veriyi işle 
            reason = form.cleaned_data['content']
            reporter = request.user


            # Yeni bir Raporlanmış Yorum örneği oluşturun ve veritabanına kaydedin
            ReportedComment.objects.create(
                reported_comment=comment,
                reporter=reporter,
                reason=reason
            )

            
            return redirect('homepage')  
    else:
        form = ReportCommentForm()

    
    return render(request, 'report_comment.html', {'form': form, 'comment_id': comment_id, 'reported_comments': reported_comments})
#yetkilendirme bölümü biter



def giris(request):


    if request.method == 'POST':
        
        kullaniciadi = request.POST.get('k_adi')
        sifre = request.POST.get('k_sifre')

        if kullaniciadi and sifre:

            user = authenticate(request, username = kullaniciadi, password = sifre)

            if user:
                login(request, user) #section, cookie vs bunları requeste koyar
                return redirect('homepage')
            else:
                return redirect('loginpage')

    else:

        return render(request, 'login.html')

def cikis(request):

    logout(request)
    return redirect('homepage')    


def kayitOl(request):

    context = {}

    if request.method == 'POST':

        form = KayitForm(request.POST)

        if form.is_valid():
            
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"] 

            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            siteuser = SiteUser(user=user, is_banned=False)
            user = form.save(commit=False)
            siteuser.save()
                    
            
            return redirect('loginpage')
        
        else:
            print("form hatası:", form.errors)
            return redirect('registerpage')


    else:
        context['form'] = KayitForm()
        return render(request, 'register.html', context)
    

def homepage(request):

    site_user = SiteUser.objects.all()
    inactive_users = SiteUser.objects.filter(is_active=False)
    moderator_users = SiteUser.objects.filter(is_moderator=False)

    context = {

        'moderator_users': moderator_users,
        'inactive_users': inactive_users,
        'site_user' : site_user

    }
    
    
    allTopics = Tweet.objects.all()

    context['content'] = allTopics
    return render(request, 'index.html', context)

    
@login_required(login_url='loginpage')  
def share_tweet(request):
    # Kullanıcının aktif olup olmadığını kontrol eder.
    inactive_user = SiteUser.objects.filter(is_active=True, user__username=request.user).exists()
    
        # kullanıcı onaylanmamışsa error verir 
    if inactive_user:



    
        if request.method == 'POST':
            form = TweetForm(request.POST, request.FILES)
            if form.is_valid():
                # Tweeti kaydeder
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()

                # Kaydettikten sonra Anasayfaya yönlendirir
                return redirect('homepage')
            else:
                # Form yoksa error verir 
                print("Form errors:", form.errors)
                messages.error(request, 'Lütfen geçerli bir tweet giriniz.')

        else:
            form = TweetForm()

        return render(request, 'tweet.html', {'form': form})      


    else:
        messages.error(request, 'Lütfen Admin onayı bekleyiniz.')

        return redirect('homepage')



   
    

def profile(request, profileName, *args, **kwargs):
    # İlgili profileName'e sahip kullanıcıyı çekin veya 404 hatası verin
    site_user = get_object_or_404(SiteUser, user__username=profileName)

    if site_user.is_active:
        # Kullanıcının tweet'lerini çekin
        user_tweets = Tweet.objects.filter(user=site_user.user)
        user_bio = site_user.bio
        data = {
            'site_user': site_user,
            'user_tweets': user_tweets,
            'user_bio': user_bio 
        }
        return render(request, 'profile.html', data)
    else:
        messages.error(request, 'Lütfen Admin sizi onaylayana kadar bekleyin')
        return redirect('homepage')
   


def edit_bio(request):
    user = request.user  # Kullanıcının oturum açtığını varsayalım
    site_user = SiteUser.objects.get(user=user)

    if request.method == 'POST' :
        form = profilePage(request.POST, request.FILES, instance=site_user)
        if form.is_valid():
            user_profile = form.save(commit=False)
            
            # Şifre güncelleme
            password = form.cleaned_data.get("password")
            if password:
                user = request.user
                user.set_password(password)
                user.save()
            
            # E-posta güncelleme
            new_email = form.cleaned_data.get("email")
            if new_email:
                user.email = new_email
                user.save()

            user_profile.save()

            messages.success(request, "Profil başarıyla güncellendi.")
            return redirect('profilepage', profileName=user.username)
        else:
            messages.error(request, "Formu doğru şekilde doldurunuz.")

    else:
        form = profilePage(instance=site_user)

    return render(request, 'edit.html', {'form': form})




def edit_tweet(request, post_id):
    user = request.user
    tweet = get_object_or_404(Tweet, id=post_id)

    if request.method == 'POST':
        form = TweetEditForm(request.POST, instance=tweet)
        if form.is_valid():
            if user == tweet.user or request.user.is_superuser: 
                form.save()
                return redirect('profilepage', profileName = user.username)
            else:
                messages.error(request, 'Bu Tweeti düzenlemek için yetkiniz bulunmamaktadır.')

    else:
        form = TweetEditForm(instance=tweet)

    return render(request, 'edit-tweet.html', {'form': form, 'tweet': tweet})



def delete_post(request, post_id):
    # Veritabanından gönderi örneğini al
    post = get_object_or_404(Tweet, id=post_id)

    # Kullanıcının gönderiyi silme iznine sahip olup olmadığını kontrol et (bu kısmı özelleştirebilirsiniz)
    if request.user == post.user or request.user.is_superuser:
        # Gönderiyi sil
        post.delete()
        messages.success(request, 'Gönderi başarıyla silindi.')
    else:
        messages.error(request, 'Bu gönderiyi silme izniniz yok.')

    return redirect('homepage')


def create_comment(request, post_id):
    tweet = get_object_or_404(Tweet, id=post_id)
    comment_list = Comment.objects.all()
    inactive_user = SiteUser.objects.filter(is_active=True, user=request.user).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if inactive_user:
                comment.user = request.user
                comment.tweet = tweet
                comment.save()
                tweet.answers += 1
                tweet.save()
                
            else:
                messages.error(request,'Lütfen Admin onayı bekleyiniz.')
                
        return redirect('homepage')       

    else:
        form = CommentForm()

    return render(request, 'comment.html', {'form': form, 'tweet': tweet, 'comment_list': comment_list})



def like(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    inactive_user = SiteUser.objects.filter(is_active=True, user=request.user).exists()

    post = Tweet.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if inactive_user:

        if like_filter is None:
            new_like = LikePost.objects.create(post_id=post_id, username=username)
            new_like.save()
            post.like = post.like + 1
            post.save()
            
        else:
            like_filter.delete()
            post.like = post.like - 1
            post.save()
                   
        
    else:
        messages.error(request, 'Lütfen Admin onayı bekleyiniz')

    return redirect('homepage')        



def edit_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            if request.user == comment.user or request.user.is_superuser:
                form.save()
                return redirect('homepage')
            else:
                messages.error(request, 'Bu yorumu düzenlemek için yetkiniz bulunmamaktadır')
                
            
            
            

    else:
        form = CommentEditForm(instance=comment)

    return render(request, 'edit-comment.html', {'form': form, 'comment': comment})




def delete_comment(request, comment_id):
    # Database içerisindeki yorumu çeker 
    comment = get_object_or_404(Comment, id=comment_id)
    tweet = comment.tweet


    # Kullanıcının yetkisi olup olmadığını ya da yorumu atan kişi olup olmadığını kontrol eder
    if request.user == comment.user or request.user.is_superuser:
        # Delete the post
        
        comment.delete()
        tweet.answers = tweet.answers - 1
        tweet.save()
        messages.success(request, 'Yorumunuz Silindi.')
    else:
        messages.error(request, 'Bu yorumu silmek için yetkiniz bulunmamaktadır.')

    return redirect('homepage')