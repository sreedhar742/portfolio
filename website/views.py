from django.shortcuts import render, redirect
from website.models import Contact  
from django.contrib import messages
from django.http import FileResponse, Http404
import os
from django.conf import settings
from .models import DownloadLog

# Create your views here.


def contact_view(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()

        # Print to console (for debugging purposes)
        print(name, email, subject, message)

        # Success message
        messages.success(request, "Your message has been sent. Thank you!")

        # Redirect to the same page or another page
        return redirect('contact')  # Replace 'contact' with the name of your URL pattern for the contact form

    # For GET requests, render the contact form
    return render(request, 'landing.html')


# def download_resume(request):
    
#     file_path = settings.RESUME_FILE_PATH
#     file_name = 'resume.pdf'

#     if not os.path.exists(file_path):
#         raise Http404("Resume file not found.")
    
#     try:
#         # Create a FileResponse without Content-Disposition
#         response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        
#         # Log the download action
#         ip_address = request.META.get('REMOTE_ADDR')
#         DownloadLog.objects.create(file_name=file_name, ip_address=ip_address)
        
#         return response
#     except Exception:
#         raise Http404("Error accessing the resume file.")

def download_resume(request):
    file_path = settings.RESUME_FILE_PATH
    file_name = 'resume.pdf'

    if not os.path.exists(file_path):
        raise Http404("Resume file not found.")
    
    try:
        # Create a FileResponse
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        
        # Log the download action using X-Forwarded-For header
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        DownloadLog.objects.create(file_name=file_name, ip_address=ip_address)
        
        return response
    except Exception:
        raise Http404("Error accessing the resume file.")




def landing(request):
    return render(request, 'landing.html')
