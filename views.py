from app.forms import*
from django.http import HttpResponse

def register_page(request):
	if reguest.method == 'POST'
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = user.objects.create_user(username = form.cleaned_data['username'], password = form.cleaned_data['password1'], email = form.cleaned_data['Email'], location = form.cleaned_data['Location'], occuption = form.cleaned_data['Occuption'], organization = form.cleaned_data['Organization'])
			return HttpResponseRedirect('/')
	
