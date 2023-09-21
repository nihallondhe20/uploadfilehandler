from django.shortcuts import render , redirect ,HttpResponseRedirect
from .models import Buyerdata,store
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import Buyerdataform,storeform
from django.contrib.auth import authenticate, login ,logout
import pandas as pd
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
@login_required
def uploadcsv(request):
    if request.method == 'POST':
        
        try:
            form = storeform(request.POST, request.FILES)
            excel_file = request.FILES['file']
            data = pd.read_excel(excel_file)
            
            print('working')
            for index, row in data.iterrows():
                # date = str(row['Date']).strip()
                # total_amount =str(row['Particulars'])
                # datas = {}
                # if date :
                #     datass = {date:[]}
                #     if date == 'NaT':
                #         datass =  date[total_amount]
                #     print(datass)
                   
                # datas = datass
                
                    
                date = str(row['Date']).strip()
                buyer = str(row['Consignee/Buyer']).strip()
                address = str(row['Address'])
                total_amount =str(row['Gross Total'])
                
                
                if (date != "NaT"):
                    user = Buyerdata(date=date, buyer=buyer, address=address,total_amount=total_amount)
                    user.full_clean() # Validate fields
                    user.save()
                    
            if form.is_valid():
                form.save()
                return redirect('/home')  # Redirect to a success page or any other page
        except Exception as e:
            messages.error(request, 'Unable to upload file. ' + repr(e))
    else:
        form = storeform()
    return render(request, 'fileupload.html', {'form': form})


@login_required(login_url='/login')
def home(request):
   
        
        users = Buyerdata.objects.all()
        
    
        # Search functionality
        search_query = request.GET.get('search')
        uname = request.GET.get('name')
        address = request.GET.get('address')
        total = request.GET.get('Total')
        ID = request.GET.get('ID')
        datee = request.GET.get('date')
        if search_query:
            users = users.filter(address__icontains=address)
            context = {'users': users}
            return render(request, 'home.html', context)
        elif search_query:
            users = users.filter(address__icontains=address)
            context = {'users': users}
            return render(request, 'home.html', context)
        elif total:
            users = users.filter(total_amount__icontains=total)
            context = {'users': users}
            return render(request, 'list.html', context)
        elif ID:
            users = users.filter(id__icontains=ID)
            context = {'users': users}
            return render(request, 'home.html', context)
        elif datee:
            users = users.filter(date__icontains=datee)
            context = {'users': users}
            return render(request, 'home.html', context)
        elif uname:
            users = users.filter(buyer__icontains=uname)
            context = {'users': users}
            return render(request, 'list.html', context)
        
        user_list = Buyerdata.objects.all()
        paginator = Paginator(user_list, 10)  # Show 10 users per page

        page = request.GET.get('page')
        users = paginator.get_page(page)
        
        context = {'users': users}
        return render(request, 'list.html', context)
    
    


def delete_all_users(request):
    if request.method == 'GET':
        # Delete all records from the User table
        Buyerdata.objects.all().delete()
        return redirect('/')  # Redirect to the home page or any other appropriate URL

    return render(request, 'delete_all_users.html')  # Replace 'delete_all_users.html' with your template name

        






def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/home')  # Redirect to a success page (change 'home' to your desired URL name)
        else:
            error_message = "Invalid username or password."
            return render(request, 'index.html', {'error_message': error_message})
    
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('/login')