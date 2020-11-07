from django.shortcuts import render,redirect
from .forms import RegisterForm, SigninForm
from .models import RegisterModel
def homepage(request):
    form = RegisterForm(request.POST or None)
    form2 = SigninForm(request.POST)
    if form.is_valid():
    	form.save()
    	form = RegisterForm()
    else:
    	if request.method == 'POST':
	    	query_email=request.POST.get("email")
	    	try:
	    		obj=RegisterModel.objects.get(email=query_email)
	    		if obj.password==request.POST.get("password"):
	    			return redirect("search")
		    	else:
		    		form2=SigninForm()
		    		context={'form':form, 'form2':form2,'login_failed':True,'Incorrect_email':False}
		    		return render(request,'homepage.html',context)
	    	except Exception as ex:
	    		print(ex)
	    		form2=SigninForm()
	    		context={'form':form, 'form2':form2,'login_failed':False,'Incorrect_email':True}
	    		return render(request,'homepage.html',context)

	    	
    context={'form': form,'form2': form2,'login_failed':False,'Incorrect_email':False}
    return render(request,'homepage.html',context)
