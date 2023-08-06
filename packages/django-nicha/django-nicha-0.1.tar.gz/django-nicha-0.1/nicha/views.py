from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login


# Create your views here.
# rest full APIS 




#============== index page===================================================
def index(request):
	return render(request,'nicha/index.html',locals())

#============== faq page=====================================================
def faq(request):
	return render(request,'nicha/faq.html',locals())

#============== mobile page==================================================
def mobile(request):
	return render(request,'nicha/mobile.html',locals())


#============== terms and conditions page====================================
def terms_and_conditions(request):
	return render(request,'nicha/terms.html',locals())
#============== privacy policy page==========================================
def privacy_policy(request):
	return render(request,'nicha/privacy.html',locals())
	
#============== how it works page ===========================================
def how_it_works_page(request):
	return render(request,'nicha/how_it_works.html',locals())

#============== community page ==============================================
def community_page(request):
	return render(request,'nicha/community.html',locals())

# # ============= Sign in page ================================================
# def sign_in_page(request):
# 	return render(request,'nicha/sign_in.html',locals())
# #============== Register page ===============================================
# def register_page(request):
# 	return render(request,'nicha/register.html',locals())

# ============= Account =====================================================
def account(request):
	return render(request,'nicha/account.html',locals())

#============== SignIn ======================================================
def sign_in_to_account(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
	else:
		pass
	return redirect("/")

#============== SignOut =====================================================
def sign_out(request):
	logout(request)
	return redirect("/")

#============= Register =====================================================
def create_account(request):
	username = request.POST['username']
	password = request.POST['password']
	email = request.POST['email']
	user = User.objects.create_user(username,email,password)
	user.save()
	return redirect("/")

