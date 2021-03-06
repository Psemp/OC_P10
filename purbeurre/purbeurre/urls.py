"""purbeurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from research import views as research_views
from account import views as ac_views
#  from products import views as product_views

###
# Trigger error for sentry
###

def trigger_error(request):
    divion_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', ac_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('profile/', ac_views.profile, name='profile'),
    path('', research_views.index, name='index'),
    path('detail/', include('products.urls')),
    path('compare/', include('research.urls')),
    path('search/', research_views.search, name='search'),
    path('mentions_legales/', research_views.legal, name='legal'),
    path('sentry-debug/', trigger_error),
]

if settings.DEBUG:  # FOR TEST PURPOSE, REMOVE FOR PROPER ERROR HANDLING AND DEPLOYMENT
    handler404 = research_views.error_404

    handler500 = research_views.error_500

    handler403 = research_views.error_403

    handler400 = research_views.error_400

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
