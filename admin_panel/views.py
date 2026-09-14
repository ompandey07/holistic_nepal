from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from users.wrapper import advance_security_wrapper


#!- ADMIN DASHBOARD CLASS BASED VIEW PROTECTED WITH ADVANCE SECURITY WRAPPER
@method_decorator(advance_security_wrapper(allowed_roles=['ADMIN', 'CASHIER', 'DELIVERY_MAN', 'MANAGER', 'STAFF']), name='dispatch')
class AdminDashboardView(View):

    def get(self, request):
        #!- RENDER ADMIN DASHBOARD HTML TEMPLATE FOR AUTHORIZED EMPLOYEES AND SUPERUSERS
        return render(request, 'admin/Dashboard/dashboard.html')
