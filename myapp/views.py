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
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.conf import settings
import razorpay

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
@permission_classes([AllowAny])
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

def order_success(request):
    return render(request, 'order_success.html')
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def place_order(request):
    if request.method == "POST":
        recipe = request.POST['recipe']
        price = int(request.POST['price']) * 100  # in paise
        qty = int(request.POST['qty'])
        total = price * qty // 100
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']

        payment = client.order.create({
            'amount': price * qty,
            'currency': 'INR',
            'payment_capture': '1'
        })

        request.session['order'] = {
            'recipe': recipe,
            'qty': qty,
            'price': total,
            'name': name,
            'phone': phone,
            'address': address
        }

        return render(request, 'payment.html', {
            'payment': payment,
            'key': settings.RAZORPAY_KEY_ID,
            'amount': price * qty,
            'recipe': recipe,
            'name': name
        })

    return render(request, 'order.html')

@csrf_exempt
def payment_success(request):
    order = request.session.get('order')
    if order:
        send_mail(
            f"New Order: {order['recipe']}",
            f"Name: {order['name']}\nPhone: {order['phone']}\nQty: {order['qty']}\nAddress: {order['address']}\nTotal: ₹{order['price']}",
            settings.EMAIL_HOST_USER,
            ['adminemail@gmail.com']
        )
    return render(request, 'order_success.html')