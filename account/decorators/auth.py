from django.shortcuts import redirect

def unauthenticated_user(func):

    def wrapper_func(request):
        print("Key check: ", request.session.has_key('customer_id') )
        if request.session.has_key('customer_id'):  
            print("decorator:", request.session['customer_id']) 
            return redirect('home')
        else:
            # response = func(request) 
            # return response
            return func(request)

    return wrapper_func