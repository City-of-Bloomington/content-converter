from django.shortcuts import render

# Create your views here.
from models import Topic

def index(request):
    results = ''

    topic_options = Topic.objects.all()

    context = {
        'topics': topic_options,
        #'results': results,
        }
    return render(request, 'topics-index.html', context)

def details(request, topic_tag=None):
    results = ''

    topic_options = Topic.objects.filter(name=topic_tag)

    if not len(topic_options):
        raise Http404("Topic does not exist: %s" % topic_tag)

    cur_topic = topic_options[0]

    context = {
        'topic': cur_topic,
        #'results': results,
        }

    return render(request, 'topics-detail.html', context)

