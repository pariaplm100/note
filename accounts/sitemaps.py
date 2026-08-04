from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap2(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return [
          "accounts:login",
          "accounts:logout",
          "accounts:signup",
          "accounts:login_page",
          "accounts:verify_email",
          "accounts:forgot_password",
          "accounts:verify_reset_password",
          "accounts:new_password",
            ]

    def location(self, item):
        return reverse(item)
