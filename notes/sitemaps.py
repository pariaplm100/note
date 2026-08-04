from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return [
            "notes:AboutUs", 
            "notes:ContactUs",
            "notes:profile",
            "notes:confirm_delete_account",
            "notes:view_profile",
            "notes:delete_account",
            "notes:verify_delete_account",
            "notes:create_note",
            "notes:create_note_in_CourseNote",
            "notes:home_notes_api",
            ]

    def location(self, item):
        return reverse(item)
