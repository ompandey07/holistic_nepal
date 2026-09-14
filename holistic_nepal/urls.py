#-- URL CONFIGURATION FOR HOLISTIC_NEPAL PROJECT ---

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#-- MAIN URL PATTERNS ---
urlpatterns = [
    path('admin/', admin.site.urls),

    #-- APP ROUTES ---
    path('', include('core.routes')),
    # path('users/', include('users.routes')),
    # path('security/', include('security.routes')),
    # path('admin-panel/', include('admin_panel.routes')),
]

#-- STATIC AND MEDIA FILES (LOCAL DEVELOPMENT) ---
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)