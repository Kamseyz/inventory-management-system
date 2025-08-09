from django.shortcuts import render,redirect
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponse


User = get_user_model()


# Create your views here.

# INDEX PAGE
class IndexPage(TemplateView):
    template_name = 'index.html'

# Login and check if it an admin or a worker and redirect them to the respective page 
class LoginUser(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    
    def form_valid(self, form):
        super().form_valid(form)
        user = self.request.user
        
        # now check their role 
        
        if user.role == "admin":
            return redirect('admin-dashboard')
        
        elif user.role == "worker":
            messages.success(self.request, 'Welcome back')
            return redirect ('worker-dashboard')
        else:
            messages.error(self.request, 'Unknow user')
            return redirect('login')
        
# login snippet for my ajax
def login_form_partial(request):
    form = LoginForm()
    html = render_to_string('accounts/login_form_partial.html', {'form': form}, request=request)
    return HttpResponse(html)
        
        

            
    


#logout users
@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('login')