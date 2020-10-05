from django.shortcuts import render
from .models import Setting

# Create your views here.

def setting(request):
	site_setting = Setting.objects.get(pk=1)
	context = {
		'settings': site_setting
	}
	return render(request, 'blog/footer.html', context)