from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'craigslist/base.html')

def search(request):
    s = request.POST.get('search')
    print(s)
    return render(request,'craigslist/search.html')