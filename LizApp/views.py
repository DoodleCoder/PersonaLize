from pyshorteners import Shortener
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Wallet, Transaction, Entry, Diary
from datetime import datetime as dt
import calendar
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


def index(request):
	return HttpResponse("Youre at the site")

@csrf_exempt
def login_site(request):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			pre = (request.META.get('HTTP_REFERER','/'))
			print(pre)
			pre = pre.split('/')
			prev = pre[-2]
			if prev == "login":
				return redirect('/index/')
			else:
				return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
		else:
			context = {}
			context['error'] = "Wrong Credentials"
			return render(request, 'login.html',context)
	else:
		if request.user.is_authenticated():
			return redirect
		context = {}
		context['error'] = ''
		return render(request,'login.html', context)

@csrf_exempt
def logout_site(request):
	logout(request)
	pre = (request.META.get('HTTP_REFERER','/'))
	pre = pre.split('/')
	prev = pre[-2]
	if prev == "logout":
		return redirect('/index/')
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
	
 	
@csrf_exempt
def register(request):
	if request.method == 'POST':
		firstName = request.POST['fname']
		lastName = request.POST['lname']
		username = request.POST['email']
		password = request.POST['password']
		user = User.objects.create(
				username = username,
				first_name = firstName,
				last_name = lastName
			)
		user.set_password(password)
		user.save()
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			diary = Diary.objects.create(
				author=user,
			)
			wallet = Wallet.objects.create(
				owner=user,
			)
			return redirect('/index/')
	else:
		return render(request, 'register.html')


@csrf_exempt
def shortenUrl(request):
	if request.method == 'POST':
		url=request.POST['longUrl']
		Longurl="http://"+str(url)
		api_key="AIzaSyAVkQ401vFyigtIrr0WdWmrN_AayRID4tk"
		shortener = Shortener('Google',api_key=api_key)
		short = (shortener.short(Longurl))
		context = {
			'text' : 'The Shortened URL is : ',
			'short' : short,
		}
		print(context)
		return render(request, 'URLedit.html', context)
	else:
		return HttpResponse('Not Allowed')

@csrf_exempt
def longUrl(request):
	if request.method == 'POST':
		api_key="AIzaSyAVkQ401vFyigtIrr0WdWmrN_AayRID4tk"
		shortener = Shortener('Google',api_key=api_key)
		url = request.POST['shortUrl']
		longer = (shortener.expand(url))
		context = {
			'text' : 'The Expanded URL is : ',
			'long' : longer
		}
		print(context)
		return render(request, 'URLedit.html', context)
	else:
		return HttpResponse('Not Allowed')

@csrf_exempt
def note(request):
	user = request.user
	diary = Diary.objects.get(author=user)	
	if request.method == 'POST':
		det = request.POST['details']
		day = calendar.day_name[dt.today().weekday()]
		entry = Entry.objects.create(
			diary=diary,
			details = det,
			day=day,
			)
		print(entry)
		entry.save()
		return redirect('/mydiary/')
	else:
		entries = Entry.objects.filter(diary=diary)
		print(entries)
		context = {
			'name':diary.name,
			'entries':entries,
		}
		return render(request,'myDiary.html',context)

@csrf_exempt
def money(request):
	user = request.user
	wallet = Wallet.objects.get(owner=user)
	context = {
		'no_cred' : wallet.no_cred,
		'no_deb' : wallet.no_deb,
		'balance' : wallet.balance,
	}
	if request.method == 'POST':
		amt = request.POST['amt']
		tType = request.POST['type']
		tx = Transaction.objects.create(
			wallet=wallet,
			amount=int(amt),
			tType=tType
		)
		print(tx)
		if tType == 'C':
			wallet.no_cred += 1
			wallet.balance += int(amt)
			wallet.save()
		else:
			wallet.no_deb += 1
			wallet.balance -= int(amt)
			wallet.save()
		return redirect('/wallet/')
	else:
		txs = Transaction.objects.filter(wallet=wallet)
		context['transactions'] = txs
		print(context)
		return render(request, 'wallet.html', context)



















