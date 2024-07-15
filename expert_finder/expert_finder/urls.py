from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('ExpertFinder.urls')),
    path('about/', include('ExpertFinder.urls')),
    path('contact/', include('ExpertFinder.urls')),
    path('faq/', include('ExpertFinder.urls')),
    # path('expertise/<int:pk>/', include('ExpertFinder.urls')),
    path('login/', include('ExpertFinder.urls')),
    path('logout/', include('ExpertFinder.urls')),
    path('searchresults/', include('ExpertFinder.urls')),
    path('services/', include('ExpertFinder.urls')),
    path('signup/', include('ExpertFinder.urls')),
    path('', include('ExpertFinder.urls')),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)