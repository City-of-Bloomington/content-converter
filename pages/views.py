from django.shortcuts import render

# Create your views here.
from models import Page

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

    context = {
        'page': cur_page,
        #'results': results,
        }

    return render(request, 'pages-detail.html', context)


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
