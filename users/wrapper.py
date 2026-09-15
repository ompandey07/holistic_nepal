from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse,
)
from django.shortcuts import redirect
from functools import wraps
import logging
import json
import html
import re

logger = logging.getLogger(__name__)


#!- --- CLIENT IP HELPER ---
def get_client_ip(request):
    """
    #! EXTRACTS CLIENT'S IP ADDRESS FROM HTTP REQUEST HEADERS.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    return ip


#!- --- ADVANCED INPUT SANITIZATION & SECURITY FILTERING ---
XSS_PATTERN = re.compile(
    r'<script.*?>.*?</script>|javascript:|onerror\s*=|onload\s*=|eval\(|document\.cookie|<iframe|<object|<embed',
    re.IGNORECASE | re.DOTALL,
)

SQLI_PATTERN = re.compile(
    r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|EXEC|EXECUTE|UNION)\b.*?\b(FROM|INTO|TABLE|DATABASE|WHERE)\b)|(--|\bOR\b\s+[\'"]?\d+[\'"]?\s*=\s*[\'"]?\d+|/\*|\*/)',
    re.IGNORECASE | re.DOTALL,
)

PATH_TRAVERSAL_PATTERN = re.compile(r'\.\./|\.\.\\', re.IGNORECASE)


def check_suspicious_input(value):
    """
    #! RECURSIVELY INSPECTS STRINGS, DICTS, AND LISTS FOR XSS, SQLI, OR PATH TRAVERSAL.
    #! RETURNS (IS_SUSPICIOUS: BOOL, REASON: STR).
    """
    if isinstance(value, str):
        if XSS_PATTERN.search(value):
            return True, "Potential XSS payload detected."
        if SQLI_PATTERN.search(value):
            return True, "Potential SQL Injection payload detected."
        if PATH_TRAVERSAL_PATTERN.search(value):
            return True, "Potential Path Traversal sequence detected."
    elif isinstance(value, dict):
        for k, v in value.items():
            suspicious, reason = check_suspicious_input(k)
            if suspicious:
                return True, reason
            suspicious, reason = check_suspicious_input(v)
            if suspicious:
                return True, reason
    elif isinstance(value, (list, tuple)):
        for item in value:
            suspicious, reason = check_suspicious_input(item)
            if suspicious:
                return True, reason
    return False, ""


def sanitize_input_string(value):
    """
    #! ESCAPES HTML ENTITIES FOR STRING DATA.
    """
    if isinstance(value, str):
        return html.escape(value.strip())
    elif isinstance(value, dict):
        return {k: sanitize_input_string(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [sanitize_input_string(i) for i in value]
    return value


def advance_filter(strict_mode=True):
    """
    #! DECORATOR TO INSPECT GET, POST, AND JSON PAYLOADS AGAINST XSS, SQLI, AND PATH TRAVERSAL.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            #!- INSPECT GET QUERY PARAMETERS
            suspicious, reason = check_suspicious_input(request.GET.dict())
            if suspicious:
                logger.warning(f"Security Filter Alert [IP: {get_client_ip(request)}]: GET params - {reason}")
                if strict_mode:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                        return JsonResponse({'status': 'error', 'message': f'Security Alert: {reason}'}, status=400)
                    messages.error(request, f"Security Alert: {reason}")
                    return HttpResponseBadRequest(f"Security Alert: {reason}")

            #!- INSPECT POST / JSON PAYLOADS
            if request.method in ['POST', 'PUT', 'PATCH']:
                if request.content_type == 'application/json':
                    try:
                        body_data = json.loads(request.body.decode('utf-8') or '{}')
                        suspicious, reason = check_suspicious_input(body_data)
                        if suspicious:
                            logger.warning(f"Security Filter Alert [IP: {get_client_ip(request)}]: JSON body - {reason}")
                            if strict_mode:
                                return JsonResponse({'status': 'error', 'message': f'Security Alert: {reason}'}, status=400)
                    except json.JSONDecodeError:
                        pass
                else:
                    suspicious, reason = check_suspicious_input(request.POST.dict())
                    if suspicious:
                        logger.warning(f"Security Filter Alert [IP: {get_client_ip(request)}]: POST params - {reason}")
                        if strict_mode:
                            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                return JsonResponse({'status': 'error', 'message': f'Security Alert: {reason}'}, status=400)
                            messages.error(request, f"Security Alert: {reason}")
                            return HttpResponseBadRequest(f"Security Alert: {reason}")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


#!- --- RATE LIMITING DECORATOR ---
def rate_limit(requests_limit=60, window_seconds=60, key_prefix="rl"):
    """
    #! DECORATOR FOR REQUEST RATE LIMITING BASED ON CLIENT IP AND ENDPOINT.
    #! REQUESTS_LIMIT: ALLOWED REQUESTS COUNT.
    #! WINDOW_SECONDS: TIME FRAME IN SECONDS.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            ip = get_client_ip(request)
            cache_key = f"{key_prefix}:{ip}:{request.path}"
            
            try:
                request_count = cache.get(cache_key, 0)
                if request_count >= requests_limit:
                    logger.warning(f"Rate limit exceeded for IP {ip} on {request.path}")
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                        return JsonResponse({
                            'status': 'error',
                            'message': 'Too many requests. Please slow down and try again later.'
                        }, status=429)
                    
                    messages.error(request, "Rate limit exceeded. Please wait before trying again.")
                    response = HttpResponse("Rate limit exceeded. Please try again later.", status=429)
                    response['Retry-After'] = str(window_seconds)
                    return response
                
                if request_count == 0:
                    cache.set(cache_key, 1, timeout=window_seconds)
                else:
                    try:
                        cache.incr(cache_key)
                    except ValueError:
                        cache.set(cache_key, request_count + 1, timeout=window_seconds)
            except Exception as e:
                logger.error(f"Rate limit cache error: {e}")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


#!- --- LOGIN REQUIRED WITH ALERT & ROLE DECORATOR ---
def login_required_alert(login_url='/login/', alert_message="Access denied. Please log in first.", allowed_roles=None):
    """
    #! ENFORCES USER AUTHENTICATION (DJANGO AUTH OR SESSION AUTH) WITH MESSAGE ALERTS AND ROLE RESTRICTIONS.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            is_authenticated = False
            user_role = None

            #!- 1. DJANGO STANDARD USER CHECK
            if hasattr(request, 'user') and request.user.is_authenticated:
                is_authenticated = True
                user_role = getattr(request.user, 'role', None) or ('ADMIN' if request.user.is_superuser else 'USER')
            
            #!- 2. CUSTOM SESSION-BASED CHECK (EMPLOYEE / PUBLIC USER)
            elif request.session.get('employee_id'):
                is_authenticated = True
                user_role = request.session.get('employee_role') or request.session.get('role')
            elif request.session.get('public_user_id') or request.session.get('user_id'):
                is_authenticated = True
                user_role = request.session.get('role', 'PUBLIC_USER')

            #!- UNAUTHENTICATED HANDLING
            if not is_authenticated:
                logger.info(f"Unauthenticated request to {request.path} from IP {get_client_ip(request)}")
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                    return JsonResponse({
                        'status': 'error',
                        'message': alert_message,
                        'redirect_url': login_url
                    }, status=401)
                
                messages.warning(request, alert_message)
                return redirect(f"{login_url}?next={request.path}")

            #!- ROLE VERIFICATION
            if allowed_roles:
                roles_set = {r.upper() for r in ([allowed_roles] if isinstance(allowed_roles, str) else allowed_roles)}
                if user_role and user_role.upper() not in roles_set:
                    logger.warning(f"Role unauthorized attempt by '{user_role}' on {request.path}")
                    if user_role.upper() == 'PUBLIC_USER' or request.session.get('public_user_id'):
                        return JsonResponse({'status': 'error', 'message': 'i am public'}, status=403)
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                        return JsonResponse({
                            'status': 'error',
                            'message': 'You do not have permission to perform this action.'
                        }, status=403)
                    
                    messages.error(request, "Permission Denied: Access restricted.")
                    return HttpResponseForbidden("Permission Denied: Access restricted.")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


#!- --- ALL-IN-ONE ADVANCE SECURITY CONTAINER WRAPPER ---
def advance_security_wrapper(
    login_required=True,
    login_url='/login/',
    alert_message="Please login to continue.",
    allowed_roles=None,
    rate_limit_requests=60,
    rate_limit_window=60,
    strict_filter=True,
    add_security_headers=True
):
    """
    #! UNIFIED SECURITY CONTAINER WRAPPER COMBINING:
    #! - AUTHENTICATION & ROLE VERIFICATION
    #! - RATE LIMITING
    #! - REQUEST FILTERING & SANITIZATION
    #! - SECURITY HEADERS CONTAINER
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            #!- 1. ADVANCED INPUT FILTERING
            if strict_filter:
                suspicious, reason = check_suspicious_input(request.GET.dict())
                if not suspicious and request.method in ['POST', 'PUT', 'PATCH']:
                    if request.content_type == 'application/json':
                        try:
                            body_data = json.loads(request.body.decode('utf-8') or '{}')
                            suspicious, reason = check_suspicious_input(body_data)
                        except json.JSONDecodeError:
                            pass
                    else:
                        suspicious, reason = check_suspicious_input(request.POST.dict())
                
                if suspicious:
                    logger.warning(f"Advance Security Container Blocked Request [IP: {get_client_ip(request)}]: {reason}")
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                        return JsonResponse({'status': 'error', 'message': f'Security Alert: {reason}'}, status=400)
                    messages.error(request, f"Security Alert: {reason}")
                    return HttpResponseBadRequest(f"Security Alert: {reason}")

            #!- 2. RATE LIMITING
            if rate_limit_requests and rate_limit_requests > 0:
                ip = get_client_ip(request)
                cache_key = f"adv_sec:{ip}:{request.path}"
                try:
                    count = cache.get(cache_key, 0)
                    if count >= rate_limit_requests:
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                            return JsonResponse({'status': 'error', 'message': 'Rate limit exceeded. Please slow down.'}, status=429)
                        messages.error(request, "Rate limit exceeded. Please wait a moment.")
                        return HttpResponse("Rate limit exceeded.", status=429)
                    if count == 0:
                        cache.set(cache_key, 1, timeout=rate_limit_window)
                    else:
                        try:
                            cache.incr(cache_key)
                        except ValueError:
                            cache.set(cache_key, count + 1, timeout=rate_limit_window)
                except Exception as e:
                    logger.error(f"Rate limiting cache error: {e}")

            #!- 3. AUTHENTICATION & ROLE VERIFICATION
            if login_required:
                is_auth = False
                user_role = None

                if hasattr(request, 'user') and request.user.is_authenticated:
                    is_auth = True
                    user_role = getattr(request.user, 'role', None) or ('ADMIN' if request.user.is_superuser else 'USER')
                elif request.session.get('employee_id'):
                    is_auth = True
                    user_role = request.session.get('employee_role') or request.session.get('role')
                elif request.session.get('public_user_id') or request.session.get('user_id'):
                    is_auth = True
                    user_role = request.session.get('role', 'PUBLIC_USER')

                if not is_auth:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                        return JsonResponse({'status': 'error', 'message': alert_message, 'redirect_url': login_url}, status=401)
                    messages.warning(request, alert_message)
                    return redirect(f"{login_url}?next={request.path}")

                if allowed_roles:
                    roles_set = {r.upper() for r in ([allowed_roles] if isinstance(allowed_roles, str) else allowed_roles)}
                    if user_role and user_role.upper() not in roles_set:
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
                        messages.error(request, "Permission Denied: Access restricted.")
                        return HttpResponseForbidden("Permission Denied: Access restricted.")

            #!- 4. VIEW EXECUTION
            response = view_func(request, *args, **kwargs)

            #!- 5. SECURITY HEADERS CONTAINER
            if add_security_headers and isinstance(response, HttpResponse):
                response['X-Content-Type-Options'] = 'nosniff'
                response['X-Frame-Options'] = 'DENY'
                response['X-XSS-Protection'] = '1; mode=block'
                response['Referrer-Policy'] = 'same-origin'

            return response
        return _wrapped_view
    return decorator


#!- --- CLASS-BASED VIEW MIXIN ---
class AdvanceSecurityMixin:
    """
    #! CLASS-BASED VIEW (CBV) MIXIN FOR APPLYING ADVANCE SECURITY WRAPPER SETTINGS TO DJANGO CBVS.
    """
    login_required = True
    login_url = '/login/'
    alert_message = "Please log in to continue."
    allowed_roles = None
    rate_limit_requests = 60
    rate_limit_window = 60
    strict_filter = True
    add_security_headers = True

    def dispatch(self, request, *args, **kwargs):
        @advance_security_wrapper(
            login_required=self.login_required,
            login_url=self.login_url,
            alert_message=self.alert_message,
            allowed_roles=self.allowed_roles,
            rate_limit_requests=self.rate_limit_requests,
            rate_limit_window=self.rate_limit_window,
            strict_filter=self.strict_filter,
            add_security_headers=self.add_security_headers,
        )
        def _dispatch_handler(req, *a, **kw):
            return super(AdvanceSecurityMixin, self).dispatch(req, *a, **kw)

        return _dispatch_handler(request, *args, **kwargs)
