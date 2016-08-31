import re

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db.models import Q

# Create your views here.
from models import Page, Conversion

class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = [
            'site',
            'title',
            'default_topic',
            'alias',
            'url',
            'page_type',
            'parent_page',
            #maybe admin only?
            #'status',
            'notes',
            ]

def check_pageform(pageform, request, cur_page):
    """
    additional checks that need to happen when a PageForm has been submitted
    """
    print "VALID!"
    #check url for prefixes and site information:
    #print dir(pageform)
    #print dir(pageform.fields['url'])
    url = re.sub("http://", '', pageform.cleaned_data['url'])
    url = re.sub("https://", '', url)

    #this is a place where source and destination (Sites object)
    #could be helpful
    if re.match('bloomington.in.gov/alpha', url):
        if pageform.cleaned_data['site'] != 'bloomington.in.gov/alpha':
            print "updating site to = bloomington.in.gov/alpha"
            pageform.cleaned_data['site'] = 'bloomington.in.gov/alpha'

        url = re.sub("bloomington.in.gov/alpha", '', url)

    elif re.match('bloomington.in.gov', url):
        if pageform.cleaned_data['site'] != 'bloomington.in.gov':
            print "updating site to = bloomington.in.gov"
            pageform.cleaned_data['site'] = 'bloomington.in.gov'

        url = re.sub("bloomington.in.gov", '', url)

    #check for existing page with same url:
    other_options = Page.objects.filter(url=url)

    if len(other_options):
        matched_page = other_options[0]
        if cur_page and (matched_page.id == cur_page.id):
            #the matched page is the current page... no problem
            return None

        else:
            #few other conditions that could result in this...
            #either there is no cur_page
            #or the cur_page.id != matched_page.id
            #print "Matched existing!"
            return matched_page

    else:
        
        return None

    #otherwise, should be all set to go... carry on!

#@login_required
def edit(request, page_id=None):

    page_options = Page.objects.filter(id=page_id)

    cur_page = None
    if len(page_options):
        cur_page = page_options[0]

    if request.method == 'POST':
        print "POST!"
        pageform = PageForm(request.POST, instance=cur_page,
                                    prefix='pages')

        if pageform.is_valid(): # All validation rules pass

            existing = check_pageform(pageform, request, cur_page)
            if existing:
                messages.warning(request, 'An existing page with that URL is already in the system. Here it is.')
                existing_url = reverse('pages:details', kwargs={'page_id':existing.id})
                redirect(existing_url)
            else:
                #now it's ok to save the changes:
                updated = pageform.save()

                finished_url = reverse('pages:details', kwargs={'page_id':updated.id})
                #print "Redirecting to: %s" % finished_url

                return redirect(finished_url)

    else:
        pageform = PageForm(prefix='pages', instance=cur_page)

    context = { 'pageform': pageform,
                }
    return render(request, 'pages-edit.html', context)


def destination(request, page_id, destination_id=None):
    """
    controller to set the (new) destination page for the passed in id

    similar to edit page, but slightly different processing
    """

    cur_destination = None
    destination_options = Page.objects.filter(id=destination_id)
    if len(destination_options):
        cur_destination = destination_options[0]

    page_options = Page.objects.filter(id=page_id)
    if len(page_options):
        cur_page = page_options[0]

    if request.method == 'POST':
        #print "POST!"
        pageform = PageForm(request.POST, instance=cur_destination,
                            prefix='pages')

        if pageform.is_valid(): # All validation rules pass

            existing = check_pageform(pageform, request, cur_destination)
            if existing:
                messages.warning(request, 'Found an existing destination with that URL. Setting it as a destination for source page.')
                new_destination = existing
                
            else:
                #now it's ok to save the changes:
                new_destination = pageform.save()

            #all_conversions = Conversion.objects.all()
            #print all_conversions
            
            #look for existing Conversion first!
            conversion_options = Conversion.objects.filter(source=cur_page).filter(destination=new_destination)
            print conversion_options
            if len(conversion_options):
                messages.warning(request, 'These pages are already associated')
                cur_conversion = conversion_options[0]
            else:

                #associate new_destination and cur_page via new Conversion object
                conversion = Conversion()
                conversion.source = cur_page
                conversion.destination = new_destination

                #TODO:
                #consider if notes are useful here
                #conversion.notes = '?'
                conversion.save()

                messages.info(request, 'New destination was added')

            
            finished_url = reverse('pages:details', kwargs={'page_id':cur_page.id})

            return redirect(finished_url)

    else:
        pageform = PageForm(prefix='pages', instance=cur_destination)

    context = { 'pageform': pageform,
                }
    return render(request, 'pages-edit.html', context)



def destination_delete(request, page_id, destination_id):
    """
    A way to remove the Conversion association with a source page
    and optionally delete the Destination page itself
    (or redirect to the destination page delete)
    """
    pass


def index(request):
    results = ''

    page_options = Page.objects.all()

    context = {
        'pages': page_options,
        #'results': results,
        }

    departmentpage_set = page_options[0].departmentpage_set
    print departmentpage_set.count()
    for item in departmentpage_set.all():
        print item.department.name

    return render(request, 'pages-index.html', context)

def details(request, page_id=None):
    results = ''

    page_options = Page.objects.filter(id=page_id)

    if not len(page_options):
        raise Http404("Page does not exist: %s" % page_id)

    cur_page = page_options[0]

    #this is also available as:
    #cur_page.conversion_destination_set (?)
    conversions = Conversion.objects.filter(source=cur_page)

    context = {
        'page': cur_page,
        'conversions': conversions,
        #'results': results,
        }

    return render(request, 'pages-detail.html', context)


def delete(request, page_id):
    """
    TODO:
    Work In Progress here.
    """
    page_options = Page.objects.filter(id=page_id)
    if not len(page_options):
        raise Http404("Page does not exist: %s" % page_id)
    cur_page = page_options[0]

    associated = Conversion.objects.filter(Q(source=cur_page) | Q(destination=cur_page))
    print associated

    #show form "Are you sure?"
    if request.method == 'POST':
        #print "POST!"
        deleteform = DeleteForm(request.POST, instance=cur_page,
                                    prefix='delete')

        if deleteform.is_valid(): # All validation rules pass
            pass
    else:
        deleteform = DeleteForm(prefix='delete', instance=cur_page)

    context = {
        'page': cur_page,
        'deleteform': deleteform,
        'associated': associated,
        }
    return render(request, 'pages-delete.html', context)    


def comment(request, page_id=None):

    page_options = Page.objects.filter(id=page_id)
    if not len(page_options):
        raise Http404("Page does not exist: %s" % page_id)
    cur_page = page_options[0]

    context = {
        'page': cur_page,
        }

    return render(request, 'pages-detail.html', context)

def check(request, page_id=None):
    """
    perform a check against the specified page(s)
    and cache the result in the database

    checks include:
      - status (200, 404, etc)
      - content change
      
      - old links (for pages on new site) (content section only)
    """
    pass
