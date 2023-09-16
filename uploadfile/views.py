from django.shortcuts import render , redirect ,HttpResponseRedirect
from .models import Buyerdata,store
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import Buyerdataform,storeform
import pandas as pd
from django.contrib import messages
from django.core.paginator import Paginator

def uploadcsv(request):
    if request.method == 'POST':
        
        try:
            form = storeform(request.POST, request.FILES)
            excel_file = request.FILES['file']
            data = pd.read_excel(excel_file)
            
            print(data)
            for index, row in data.iterrows():
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
    return render(request, 'upload.html', {'form': form})


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
        return render(request, 'home.html', context)
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
        return render(request, 'home.html', context)
    
    context = {'users': users}
    return render(request, 'home.html', context)
    
        


