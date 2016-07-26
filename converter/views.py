from django.shortcuts import render

# Create your views here.

def index(request):
    results = ''

    context = {
        #'pages': page_options,
        #'results': results,
        }

    return render(request, 'index.html', context )
