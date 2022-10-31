
from django.contrib import admin
from django.urls import path
from django.urls import include

#To show media files
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home_app.urls')),
    path('account/',include('login_app.urls')),
    path('admin_user/',include('admin_app.urls')),
    path('patient/',include('patient_app.urls')),
    path('doctor/',include('doctor_app.urls')),
    path('payments/',include('payment_app.urls')),
]
urlpatterns +=staticfiles_urlpatterns()
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)