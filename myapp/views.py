from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models


BASE_CRAIGSLIST_URL ='https://losangeles.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL ='https://images.craigslist.org/{}_300x300.jpg'
def home(request):
    return render(request,'craigslist/base.html')

def search(request):
    s = request.POST.get('search')
    models.Search.objects.create(search=s)

    # Dynamically creates the URL by storing the SEARCH USER INPUTS replacing spaces with +
    # user input = python tutor 
    # url = python+tutor attached to base url
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(s))
    
    # Web Scraping Begins
    # Deriving HTML / CSS from the Craigslist URL
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data,features='lxml')
    
    #Find lists of search results generated based on the given input 
    post_listings = soup.find_all('li',{'class':'result-row'})
    
    final_postings=[]
    #print("Print URL === ",final_url)     

    for post in post_listings:

        
        post_title = post.find(class_= 'result-title').text
        post_url = post.find('a').get('href')
        
        if(post.find(class_= 'result-price')):
            post_price = post.find(class_= 'result-price').text
        else :
            post_price="N/A"                        
        

        if(post.find(class_='result-image').get('data-ids')):
            post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            final_image_url = BASE_IMAGE_URL.format(post_image)
        else:
            final_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title,post_url,post_price,final_image_url))

    stuff_for_frontend = {'s':s,'final_postings':final_postings}
    return render(request,'craigslist/search.html',stuff_for_frontend)