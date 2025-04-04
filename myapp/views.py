from django.shortcuts import render, get_object_or_404,redirect
import logging
from .models import post,aboutus,img,offer,Order
from django.http  import Http404,HttpResponse
from django.core.paginator import Paginator
from .forms import ContactFrom
from django.contrib import messages
from .serializers import UserRegisterSerializer,PostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import api_view,permission_classes


# Home page view
def index(request):
    title = 'Get Delicious Food Anytime...'
    image_obj = img.objects.first()
    image_url = image_obj.imgs 
    offers = offer.objects.first().offers
    all_posts = post.objects.all()
    paginator=Paginator(all_posts,4)
    page_number=request.GET.get('page')
    page_object=paginator.get_page(page_number)
    return render(request, 'index1.html', {'title': title, 'posts': page_object,"image_url": image_url ,'offers':offers})
    


# Details page view
def details(request, slug):
   try:
    # post_instance = get_object_or_404(posts, id=post_id)  # Fetch the specific post by ID or return 404
    post_instance =post.objects.get(slug = slug)
   except post.DoesNotExist:
      raise Http404("post Dose not exit!.")
   posts= post.objects.all()
   return render(request, 'details.html', {'post': post_instance,'postes':posts})

def contact(request):
    if request.method == 'POST':
       form = ContactFrom(request.POST)
       name = request.POST.get('name')
       email = request.POST.get('email')
       msg = request.POST.get('massage')
       logger = logging.getLogger("testing")
       if form.is_valid():
          logger.debug(f"post data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['massage']}")
          success_msg = "your email has successfuly sent!"
          return render(request, 'contact.html',{'form':form, 'success':success_msg})
       else:
          logger.debug("form is invaild")
          return render(request, 'contact.html',{'form':form, 'name':name , 'emails':email , 'msg':msg})
          
       
    return render(request, 'contact.html')
def about(request):
    about_content = aboutus.objects.first().content
    return render(request, 'about.html',{'about_content':about_content})
def order(request):
   image_obj = img.objects.first()
   image_url = image_obj.imgs 
   if request.method == "POST":
        recipe_name = request.POST.get("recipe_name")
        quantity = request.POST.get("quantity")
        phone_number = request.POST.get("phone_number")
        location = request.POST.get("location")

        if recipe_name and quantity and phone_number and location:
            Order.objects.create(
                recipe_name=recipe_name,
                quantity=quantity,
                phone_number=phone_number,
                location=location,
            )
            messages.success(request, "Your order has been placed successfully!")
            return redirect("order")

   return render(request,'order.html',{"image_url": image_url})
def cart(request):
   posts = post.objects.all()
   return render(request,'cart.html',{ 'posts': posts})
def register(request):
   return render(request,'register.html')

def login(request):
   return render(request,'login.html')

def reset(request):
   return render(request,'password_reset.html')

@api_view(['POST'])
def registeruser(request):
   serializer = UserRegisterSerializer(data = request.data)
   if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
   return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
   user = request.user
   serializer = PostSerializer(data= request.data)
   if serializer.is_valid():
      serializer.save(author=user)
      return Response(serializer.data)
   return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)