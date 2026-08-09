from django.contrib.syndication.views import Feed
from django.urls import reverse
from notes.models import Note,Course,NoteFile


class LatestEntriesFeed(Feed):
    title = "Note Organizer"
    link = "/rss/feed"
    description = "A Note Organizer for Students and other people"

    def items(self):
        return Note.objects.all()

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.topic
    
    
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse("notes:news-item", args=[item.pk])
    
class LatestEntriesFeed2(LatestEntriesFeed):
    title = "Note Organizer"
    link = "/rss/courses"
    description = "A Note Organizer for Students and other people"

    def items(self):
        return Course.objects.all()

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return str(item.create_time)
    
    
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse("notes:news-item2", args=[item.pk])    
    
class LatestEntriesFeed3(LatestEntriesFeed):
    title = "Note Organizer"
    link = "/rss/notefiles"
    description = "A Note Organizer for Students and other people"

    def items(self):
        return NoteFile.objects.all()

    def item_title(self, item):
        return item.note

    def item_description(self, item):
        return item.file
    
    
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse("notes:news-item3", args=[item.pk])        