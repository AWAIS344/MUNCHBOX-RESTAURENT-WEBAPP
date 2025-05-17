from django.shortcuts import render

# Create your views here.
def BlogHome(request):
    context={}
    return render(request,"blog/blog.html",context)