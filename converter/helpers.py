import re

def to_tag(item):
    """
    take any string and convert it to an acceptable tag

    tags should not contain spaces or special characters
    numbers, lowercase letters only
    underscores can be used, but they will be converted to spaces in some cases
    """
    item = item.lower()
    #get rid of trailing and leading blank spaces:
    item = item.strip()
    item = re.sub(' ', '_', item)
    item = re.sub("/", '_', item)

    item = re.sub("\?", '', item)

    #there are times when it is useful to have a dash in a tag...
    #removing should be left to caller:
    #item = re.sub("\-", '_', item)
    
    item = re.sub("\\\\'", '', item)
    item = re.sub("\\'", '', item)
    item = re.sub("'", '', item)

    #unicode characters don't often agree with tags
    #comment out if you want to keep them
    item = re.sub(r'[^\x00-\x7F]+', ' ', item)

    #too many sources of problems with this sequence
    item = re.sub("&amp;", 'and', item)
    #even this seems like it could re-introduce issues:
    item = re.sub("&", 'and', item)

    #difficult to replace 
    #sre_constants.error: unbalanced parenthesis
    #item = re.sub(re.escape('('), '', item)
    #item = re.sub(re.escape(')'), '', item)
    
    item = re.sub('[()]', '', item)

    #could consider filtering ':' and '?'
    #these characters don't play well with command lines
        
    return item
