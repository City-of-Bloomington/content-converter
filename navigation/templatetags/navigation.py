from django import template

#now we can import models and views from other applications in this project:

register = template.Library()

#https://docs.djangoproject.com/en/stable/howto/custom-template-tags/
#https://docs.djangoproject.com/en/dev/topics/forms/
def make_nav(context):
    """
    this is meant to be called on every request
    determine if we know the current location or not
    then generate the navigation accordingly
    """

    #print dir(context)
    request = context['request']
    
    stored = request.session.get('location', default=None)
    #print "Stored location: %s" % stored
    
    #list of tuples: (link, content)
    #nav_items = [ ('/', "Home") ]
    nav_items = [ ]

    if stored:
        #show any navigation items that are location specific

        #nav_items.append( ('/location/%s' % stored['tag'], "Map") )
        #nav_items.append( ('/location/%s/resources' % stored['tag'], "Resources") )

        #select_form.fields['choice'].initial = stored['tag']
        pass
    else:
        #nav_items.append( ('/location/', "Map") )
        pass

    nav_items.append( ('/pages/', "Pages") )
    nav_items.append( ('/departments/', "Departments") )
    nav_items.append( ('/topics/', "Topics") )
    ## nav_items.append( ('//', "") )
    ## nav_items.append( ('//', "") )
    ## nav_items.append( ('//', "") )

    return { 'items': nav_items, 'user': request.user }

register.inclusion_tag('navigation.html', takes_context=True)(make_nav)


