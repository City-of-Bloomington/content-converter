from django.http import Http404
from django.shortcuts import render

# Create your views here.
from models import Department

def index(request):
    results = ''

    department_options = Department.objects.all()

    context = {
        'departments': department_options,
        #'results': results,
        }

    return render(request, 'departments-index.html', context )

def pages(request, department_tag=None):
    results = ''

    department_options = Department.objects.filter(tag=department_tag)
    #print department_options

    if not len(department_options):
        raise Http404("Department does not exist: %s" % department_tag)

    department = department_options[0]
    #print dir(department)
    #print department.departmentpage_set
    #print department.departmentpage_set.count()

    #TODO:
    #probably a more elegant way to do this...
    pages = []
    department_pages = department.departmentpage_set.all()
    for department_page in department_pages:
        pages.append(department_page.page)
    
    context = {
        'department': department,
        'pages' : pages
        #'results': results,
        }

    return render(request, 'departments-pages.html', context )
