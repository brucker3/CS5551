from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
	# return HttpResponse('Homepage')
	return render(request,'homepage.html')
	
def game(request):
	# return HttpResponse('game')
	return render(request,'game.html')
	
	