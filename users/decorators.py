from functools import wraps
from django.shortcuts import redirect
from .models import User

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        username = request.session.get('username')
        is_logined = request.session.get('logged_in')

        if not is_logined or not username or is_logined == False:
            return redirect('user:signin')
        
        user = User.objects(username=username).first()
        if not user:
            request.session.flush()
            return redirect('user:signin')
        
        request.user = user
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view