from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.core.files.storage import FileSystemStorage
import os
import pymysql
from datetime import date
from django.contrib import messages  # To display messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import cv2
from skimage.metrics import structural_similarity as ssim
#database connection
signverifydb = pymysql.connect(host="localhost", user="root", password="root", database="signature_verification_system_db")
cursor = signverifydb.cursor()

#index page content start
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def user_registration(request):
    return render(request,"user_registration.html")

def submit_user_registration_details(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email already exists in the database
        cursor.execute("SELECT * FROM user_registration_details WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render(request, "user_registration.html", {
                "error": "Email already exists. Please try again with a different email."
            })

        # Check if the password already exists in the database
        cursor.execute("SELECT * FROM user_registration_details WHERE password = %s", (password,))
        existing_password = cursor.fetchone()

        if existing_password:
            # No need to iterate — just show the message
            return render(request, "user_registration.html", {
                "error": "Password already used. Please choose a different password."
            })

        # Insert new user details into the database
        cursor.execute(
            "INSERT INTO user_registration_details (name, contact, email, password) VALUES (%s, %s, %s, %s)",
            (name, contact, email, password)
        )
        signverifydb.commit()

        return render(request, "user_login.html", {"success": "Registration successful!"})

    return render(request, "user_registration.html")

def user_login(request):
    return render(request,"user_login.html")

def submit_user_login_details(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    email=email.strip()
    password=password.strip()
    user=""
    sql="select * from user_registration_details";
    c1=signverifydb.cursor()
    c1.execute(sql)
    rows=c1.fetchall()
    ispresent=False
    for x in rows:
        print(x)
        if(email.strip()==x[3] and password.strip()==x[4]):
            request.session['username'] =x[1]
            
            ispresent=True
            break
    if (ispresent):
        return render(request,"user_dashboard.html",{'u':user})
    else:
        return render(request,"user_login.html")
    
def admin_login(request):
    return render(request,"admin_login.html")

def submit_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if both username and password are "admin"
        if username == "admin" and password == "admin":
            # If successful, redirect to the dashboard
            messages.success(request, 'Login successful!')
            return redirect('admin_dashboard')  # Adjust this if the dashboard path is different
        else:
            # If invalid, show an error message
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, "admin_login.html")

# index page content end

# user dashboard menu start
def user_dashboard(request):
    return render(request,"user_dashboard.html")

def upload_signature(request):
    uname=request.session['username']
    if request.method == 'POST' and request.FILES['signature_image']:
        name = request.POST['name']
        
        signature_image = request.FILES['signature_image']

        # Save the signature image
        fs = FileSystemStorage()
        filename = fs.save(signature_image.name, signature_image)
        file_url = fs.url(filename)

        # Insert the signature details into the database
        cursor.execute("INSERT INTO user_signature_details (name, signature_path) VALUES (%s, %s)", (name, file_url))
        signverifydb.commit()

        messages.success(request, 'Signature uploaded successfully!')
        return render(request, 'upload_signature.html')

    return render(request, 'upload_signature.html',{'name':uname})

def preprocess_image(image_path):
    # Load the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"Failed to load image from {image_path}. The file may be missing or corrupt.")
        return None  # Return None if image loading fails

    # Resize the image
    img_resized = cv2.resize(img, (300, 100))

    # Apply thresholding to convert to black-and-white (binary) image
    _, img_thresholded = cv2.threshold(img_resized, 127, 255, cv2.THRESH_BINARY)

    return img_thresholded

def verify_signature(request):
    result = None
    if request.method == 'POST' and request.FILES['signature_image']:
        uploaded_image = request.FILES['signature_image']

        # Save the uploaded image temporarily
        fs = FileSystemStorage()
        uploaded_image_name = fs.save(uploaded_image.name, uploaded_image)
        uploaded_image_path = fs.path(uploaded_image_name)

        # Preprocess the uploaded image
        uploaded_img_processed = preprocess_image(uploaded_image_path)
        if uploaded_img_processed is None:
            result = "Failed to process uploaded signature image."
            return render(request, 'verify_signature.html', {'result': result})

        # Compare with stored images
        matching_user = None
        highest_ssim = -1
        cursor.execute("SELECT * FROM user_signature_details")
        rows = cursor.fetchall()

        for row in rows:
            # Correct the path construction here
            stored_image_path = os.path.join(settings.BASE_DIR, row[2].lstrip('/'))  # Correct path
            print(f"Checking stored signature path: {stored_image_path}")
            
            if not os.path.exists(stored_image_path):
                print(f"Stored image not found: {stored_image_path}")
                continue  # Skip this iteration if the image doesn't exist

            stored_img_processed = preprocess_image(stored_image_path)
            if stored_img_processed is None:
                print(f"Failed to process stored signature image: {stored_image_path}")
                continue  # Skip this iteration if image processing fails

            # Compute SSIM between the processed images
            ssim_value, _ = ssim(uploaded_img_processed, stored_img_processed, full=True)

            if ssim_value > highest_ssim:
                highest_ssim = ssim_value
                matching_user = row

        if matching_user and highest_ssim > 0.85:  # Threshold SSIM value, adjust as needed
            result = f"Signature verified! The name of the user is {matching_user[1]}."
        else:
            result = "No match found for the signature."

        # Clean up uploaded temporary file
        os.remove(uploaded_image_path)

    return render(request, 'verify_signature.html', {'result': result})

def user_logout(request):
    return render(request,"index.html")
#user dashboard menu end
#admin dashboard menu start
def admin_dashboard(request):
    return render(request,"admin_dashboard.html")


def upload_moresignature_by_admin(request):
    uname = request.GET['name']
    print(uname)
    if request.method == 'POST' and request.FILES['signature_image']:
        name = request.POST['name']
        signature_image = request.FILES['signature_image']
        
        # Save the signature image
        fs = FileSystemStorage(location='static/uploads/') 
        filename = fs.save(signature_image.name, signature_image)
        #file_url = fs.url(filename)
        file_url = f"/static/uploads/{filename}"
        print(file_url)

        # Insert the signature details into the database
        cursor.execute("INSERT INTO user_signature_details (name, signature_path) VALUES (%s, %s)", (name, file_url))
        signverifydb.commit()

        messages.success(request, 'Signature uploaded successfully!')
        return render(request, 'upload_moresignature_by_admin.html')

    return render(request, 'upload_moresignature_by_admin.html',{'name': uname})


def upload_signature_by_admin(request):
    if request.method == 'POST' and request.FILES['signature_image']:
        name = request.POST['name']
        signature_image = request.FILES['signature_image']
        
        # Save the signature image
        fs = FileSystemStorage(location='static/uploads/') 
        filename = fs.save(signature_image.name, signature_image)
        #file_url = fs.url(filename)
        file_url = f"/static/uploads/{filename}"
        print(file_url)

        # Insert the signature details into the database
        cursor.execute("INSERT INTO user_signature_details (name, signature_path) VALUES (%s, %s)", (name, file_url))
        signverifydb.commit()

        messages.success(request, 'Signature uploaded successfully!')
        return render(request, 'upload_signature_by_admin.html')

    return render(request, 'upload_signature_by_admin.html')

# Admin View Signatures
def view_users(request):
    # Query the database to fetch all signatures
    cursor.execute("SELECT * FROM user_registration_details")
    signatures = cursor.fetchall()

    return render(request, "viewusers.html", {'signatures': signatures})

# Admin View Signatures
def view_signature(request):
    # Query the database to fetch all signatures
    cursor.execute("SELECT * FROM user_signature_details")
    signatures = cursor.fetchall()

    return render(request, "view_signature.html", {'signatures': signatures})

def delete_signature(request, signature_id):
    # Get the signature details from the database
    cursor.execute("SELECT * FROM user_signature_details WHERE id = %s", (signature_id,))
    signature = cursor.fetchone()

    if signature:
        # Delete the signature record from the database
        cursor.execute("DELETE FROM user_signature_details WHERE id = %s", (signature_id,))
        signverifydb.commit()

        # Remove the corresponding image file
        file_path = os.path.join(settings.BASE_DIR, 'media', signature[2].lstrip('/'))  # Correct path
        if os.path.exists(file_path):
            os.remove(file_path)

        messages.success(request, 'Signature deleted successfully!')

    return HttpResponseRedirect(reverse('view_signature'))

def admin_logout(request):
    return render(request,"index.html")






#admin dashboard menu end
