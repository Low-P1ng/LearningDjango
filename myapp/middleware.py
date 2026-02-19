import time
from django.http.response import HttpResponseForbidden

class LogRequestMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        
    def __call__(self, request):  
        #process before
        print(f"[Middleware] Request path {request.path}")
        response = self.get_response(request)
        #process after
        print(f"[Middleware] Response status: {response.status_code}")
        return response
        
class TimerMiddleware():
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        print(f"[Middleware] Request took {duration:.2f} seconds")
        return response
    
class BlockIPMiddleware():
    BLOCKED_IPS = []
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        
        if ip in self.BLOCKED_IPS:
            return HttpResponseForbidden("Your ip is blocked")
        return self.get_response(request)
        
        