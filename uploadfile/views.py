from django.shortcuts import render , redirect ,HttpResponseRedirect
from .models import Buyerdata,store
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import Buyerdataform,storeform
import pandas as pd
from django.contrib import messages


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
    date = Buyerdata.objects.all()
    name = Buyerdata.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    uname = request.GET.get('name')
    addrss = request.GET.get('address')
    total = request.GET.get('Total')
    if search_query:
        users = users.filter(address__icontains=addrss)
        context = {'users': users}
        return render(request, 'home.html', context)
    if total:
        users = users.filter(total_amount__icontains=total)
        context = {'users': users}
        return render(request, 'home.html', context)
    if uname:
        users = users.filter(buyer__icontains=uname)
        context = {'users': users}
        return render(request, 'home.html', context)
    
    context = {'users': users}
    return render(request, 'home.html', context)
    
        


