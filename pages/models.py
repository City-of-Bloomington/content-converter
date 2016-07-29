from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from departments.models import Department
from topics.models import Topic

SITE_OPTIONS = (
    ('bloomington.in.gov/alpha', 'Alpha (destination)'),
    ('bloomington.in.gov', 'Current (source)'),
    )

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=200)

    #alpha vs. current
    #maybe it is better to just use "source" and "destination"
    #could have a different model to track where "source" and "destination" map
    #
    #however, site is also used by templates to render the full URL
    site = models.CharField(max_length=30, choices=SITE_OPTIONS, default="")

    #for a destination page, we may not know the url yet
    #if it hasn't been created
    #typically, this is just the suffix path without the site aspect
    url = models.CharField(max_length=200, blank=True)

    #hopfully, on the new alpha site, alias and url will usually match
    alias = models.CharField(max_length=50, blank=True)

    #mostly useful for destination, new, alpha site pages:
    #e.g. book page, normal page, etc
    page_type = models.CharField(max_length=30, blank=True)

    #unknown, pending, delete/ignore, migrated
    status = models.CharField(max_length=30, default="unknown")

    #similar to status... a few spreadsheets had more than one colum
    notes = models.TextField(blank=True)

    #priority for conversion? (not sure if this is useful)
    position = models.IntegerField(default=-1)

    #not sure if this should be a ForeignKey to another page
    #or just the url of the page referenced
    parent_page = models.CharField(max_length=200, blank=True)

    default_topic = models.ForeignKey(Topic, null=True)

    #comma separated list should be fine
    #these are the people who should be notified
    #for any tasks or changes to the page
    contacts = models.CharField(max_length=200, blank=True)

    
    #section_id = models.IntegerField()
    section_id = models.CharField(max_length=10, blank=True)

    #comma separated list should be fine
    #these are the categories from the original CMS
    # (found in the last columns in spreadsheets)
    #not to be confused with new topics
    #informational only
    categories = models.CharField(max_length=200)

    #keep a snapshot of what was there at the time of the last scan
    content = models.TextField(blank=True)
    last_scan = models.DateTimeField('last scanned', blank=True, null=True)
    
    added = models.DateTimeField('date published', auto_now_add=True)

    # Google analytics stats:
    #page_views = models.IntegerField(blank=True, null=True)
    #page_views = models.IntegerField()
    #easier to handle '' values with CharField... can still do similar ops
    page_views = models.CharField(max_length=10, blank=True)
    #position = models.IntegerField(default=-1)
    #page_views_unique = models.IntegerField()
    page_views_unique = models.CharField(max_length=10, blank=True)
    average_time = models.CharField(max_length=10, blank=True)
    #haven't found these as useful.
    #entrances = models.IntegerField()
    entrances = models.CharField(max_length=10, blank=True)
    bounce_rate = models.CharField(max_length=10, blank=True)
    exit_percent = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return self.title

    def full_path(self):
        base = "https://" + self.site 
        if self.alias:
            return base + self.alias
        else:
            return base + self.url


class Conversion(models.Model):
    """
    might need to make an association both ways? No...
    source should always be one site, and destination should be the other
    """

    #e.g. current CMS
    source = models.ForeignKey(Page, related_name="conversion_source_set")
    #e.g. new Drupal site
    destination = models.ForeignKey(Page, related_name="conversion_destination_set")
    
    #was there something unusual about the conversion?
    #e.g. was it a duplicate?
    notes = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return "%s moving to %s" % (self.source.title, self.destination.title)

class PageContact(models.Model):
    """
    Assciate a Page with one or more Users who should be the point of contact
    """
    page = models.ForeignKey(Page)
    user = models.ForeignKey(User)

    def __str__(self):
        return "%s: %s" % (self.page.title, self.user.name)

class DepartmentPage(models.Model):
    """
    Assciate a Page with one or more Departments
    """
    page = models.ForeignKey(Page)
    department = models.ForeignKey(Department)

    def __str__(self):
        return "%s: %s" % (self.department.name, self.page.title)

class PageTopic(models.Model):
    """
    Associate a Topic with one or more Pages
    Don't want to limit a page to only having one
    """
    page = models.ForeignKey(Page)
    topic = models.ForeignKey(Topic)

    def __str__(self):
        return "%s: %s" % (self.topic.name, self.page.title)


class Comment(models.Model):
    """
    A comment or note about a page
    """
    page = models.ForeignKey(Page)

    added = models.DateTimeField('date published', auto_now_add=True)

    content = models.TextField(blank=True)

    user = models.ForeignKey(User)


    def __str__(self):
        return "%s: %s" % (self.user.name, self.content)
