import csv 
import pandas as pd
from .models import Member, Audit
from .forms import MemberForms
from django.contrib import messages
from .forms import CSVUploadForm
from django.shortcuts import render, redirect
from .operations import parse_html, audit_main
from django.core.exceptions import ValidationError



def home(request):
    all_members = Member.objects.all
    return render(request, 'home.html',{'all':all_members})

def join(request):
    if request.method == "POST":
        form = MemberForms(request.POST or None)
        if form.is_valid():
            form.save()
        else:
             fname = request.POST['fname']
             lname = request.POST['lname']
             age = request.POST['age']
             email = request.POST['email']
             passwd = request.POST['passwd']
             messages.success(request,('There was an error in your form'))
             return render(request, 'join.html',{'fname': fname, 'lname': lname, 'age':age, 'passwd':'passwd','email':email})
        messages.success(request,('Your form has submitted succefully'))
        return redirect('home')
    else:
        return render(request, 'join.html',{})

# ********************************************************************************************************************************************
# ********************************************************************************************************************************************
# ********************************************************************************************************************************************


import os
from tempfile import NamedTemporaryFile

def audit(request):
    processed_data = None
    message = 'msg not received'
    form = CSVUploadForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        if form.is_valid():
            input_file = request.FILES['file']
            if not input_file.name.endswith('.xlsx'):
                form.add_error('file', ValidationError('File must be in .xlsx format'))
            else:
                # Save the uploaded file to a temporary location
                with NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                    for chunk in input_file.chunks():
                        temp_file.write(chunk)
                    
                    temp_file_path = temp_file.name

                try:
                    # Assuming `audit_main` requires a file path
                    processed_data = audit_main(temp_file_path)
                    message = 'file received'

                    for data in processed_data:
                        Audit.objects.create(
                            asin=data['asin'],
                            brand_name=data['brand_name'],
                            generic_name=data['generic_name'],
                            status=data['status'],
                            availablity=data['availablity'],
                            browser_node=data['browser_node'],
                            title=data['title'],
                            reviews=data['reviews'],
                            rating=data['rating'],
                            deal=data['deal'],
                            sold_by=data['sold_by'],
                            buybox=data['buybox'],
                            image_len=data['image_len'],
                            main_img_url=data['main_img_url'],
                            bullet_point_len=data['bullet_point_len'],
                            bsr1=data['bsr1'],
                            bsr2=data['bsr2'],
                            price=data['price'],
                            MRP=data['MRP'],
                            description=data['description'],
                            A_plus=data['A_plus'],
                            store_link=data['store_link'],
                        )
                finally:
                    # Clean up the temporary file
                    os.remove(temp_file_path)

    else:
        form = CSVUploadForm()

    return render(request, 'audit.html', {'form': form, 'data': processed_data, 'message': message})
