from django.contrib import admin
from django.urls import path,include
from django.contrib.sitemaps.views import sitemap
from notes.sitemaps import StaticViewSitemap
from accounts.sitemaps import StaticViewSitemap2
from notes import views
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    "static": StaticViewSitemap,
    "accounts": StaticViewSitemap2,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('',include('accounts.urls')),
    path('', include("notes.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )




    

    
