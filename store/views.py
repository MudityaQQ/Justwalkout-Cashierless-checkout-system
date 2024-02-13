from django.shortcuts import render, redirect
from Face_Recog.detection import FaceRecognition
from Face_Recog.enterFace import EnterFaceRecognition
from Face_Recog.exitFace import ExitFaceRecognition
from django.core.exceptions import ObjectDoesNotExist
from Face_Recog.models import UserProfile
from django.http import HttpResponse
from .QRcode import ProductQrCode
from django.views import View
from .models import Product
from .models import Order
from gtts import gTTS
import os
from datetime import datetime
import playsound


faceRecognition = FaceRecognition()
enterfaceRecognition = EnterFaceRecognition()
exitfaceRecognition = ExitFaceRecognition()
productQrCode = ProductQrCode()
beepfileAudioPath = "Face_Detection/static/audio/beep.mp3"

# audio function
def audioSpeaker(audioSpeaker):
    speechAudio = audioSpeaker
    language = 'en'
    dateString = datetime.now().strftime("%d%m%Y%H%M%S")
    output = gTTS(text=speechAudio, lang=language, slow=False)
    fileAudioPath = "Face_Detection/static/audio/output"+dateString+".mp3"
    output.save(fileAudioPath)
    playsound.playsound(fileAudioPath, True)
    os.remove(fileAudioPath)

# generate the invoice
# have to work on it afterwards

# user check in the store
def checkIn(request):
    try:
        face_id = enterfaceRecognition.enterFace()
        request.session['enterCustomerID'] = int(face_id)
        # audio beep
        playsound.playsound(beepfileAudioPath, True)
        # playAudioCheckInUser = "Welcome To JustWalkOut cashierless Checkout Store. Enjoy Shopping!!!. By JustWalkOut Team"
        playAudioCheckInUser = "Welcome To JustWalkOut cashierless Store"
        # playAudioCheckInUser = "Welcome Sir to justwalkout Store. hahaha i am your virtual assitance"
        audioSpeaker(playAudioCheckInUser)
        return redirect('welcome', str(face_id))
    except Exception as e:
        pass

def userWelcomePage(request):
    try:
        return render(request, 'store/userWelcomePage.html')
    except Exception as e:
        print("Error - userWelcomePage ", e)
        return render(request, 'store/userWelcomePage.html')


def welcome(request, face_id):
    try:
        data = {
            'user': UserProfile.objects.get(face_id=face_id)
        }
        return redirect('storeIndex')
    except ObjectDoesNotExist:
        return redirect('storeIndex')


def storeIndex(request):
    try:
        enterCustomerID = request.session.get('enterCustomerID')
        customers = UserProfile.getUserByID(enterCustomerID)
        print("[INFO] customer audio : ", str(customers))
        totalCustomers = UserProfile.getAllUsers()
        allProducts = Product.get_all_products()
        return render(request, 'store/storeIndex.html', {'customers': customers, 'totalCustomers': totalCustomers, 'allProducts': allProducts})
    except Exception as e:
        print("Error - storeIndex = ", e)
        return render(request, 'store/storeIndex.html')


def productInfo(request):
    try:
        productID = productQrCode.detectID()
        # set the product ID
        request.session['productID'] = productID
        # audio beep
        playsound.playsound(beepfileAudioPath, True)
        # speak the event
        productPickUpEvent = "Sir, you have picked the product"
        audioSpeaker(productPickUpEvent)

        # test1
        productID = request.session.get('productID')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(productID)
            if quantity:
                cart[productID] = quantity + 1
            else:
                cart[productID] = 1
        else:
            cart = {}
            cart[productID] = 1

        request.session['cart'] = cart
        exitCustomerID = request.session.get('exitCustomerID')
        enterCustomerID = request.session.get('enterCustomerID')
        print(request.session.get('cart').keys())
        print("[INFO] Enter Customer ID = ", enterCustomerID)
        print("[INFO] Exit Customer ID = ", exitCustomerID)
        print("[INFO] ID = ", enterCustomerID, " Cart = ", cart)
        print("[INFO] key = ", list(request.session.get('cart').keys()))
        return redirect('storeIndex')
    except Exception as e:
        print("Error - productInfo = ", e)
        return redirect('storeIndex')


class Cart(View):
    try:
        def get(self, request):
            ids = list(request.session.get('cart').keys())
            products = Product.getProductsById(ids)
            return render(request, 'store/cart.html', {'products': products})
    except Exception as e:
        print("Error - cart = ", e)


class CheckOut(View):
    try:
        def get(self, request):
            # recognised face on exit Gate
            face_id = exitfaceRecognition.exitFace()
            faceID = int(face_id)
            # create a session for exit customer ID
            request.session['exitCustomerID'] = faceID
            enterCustomerID = request.session.get('enterCustomerID')
            exitCustomerID = request.session.get('exitCustomerID')
            # checking the enterance and exit IDs
            if (enterCustomerID == exitCustomerID):
                cart = request.session.get('cart')
                print("[INFO ]cart = ", cart)
                products = Product.getProductsById(list(cart.keys()))
                print("[INFO ]customerid = ", exitCustomerID,
                      " cart = ", cart, " products = ", products)

                for product in products:
                    order = Order(product=product,
                                  customer=UserProfile(
                                  face_id=exitCustomerID),
                                  price=product.price,
                                  quantity=cart.get(str(product.idProduct)))

                    order.save()
                    # audio beep
                    playsound.playsound(beepfileAudioPath, True)
                    exitSoundPlay = "Thank you shopping with JustWalkout. Visit Again. Have a Great Day ahead. By JustWalkOut Team"
                    audioSpeaker(exitSoundPlay)
                    request.session.clear()
                    request.session['cart'] = {}
                    playsound.playsound(beepfileAudioPath, True)
                return redirect('dashboard', exitCustomerID)
    except Exception as e:
        print("Error - checkout = ", e)