import os, sys, re
sys.path.append(os.path.dirname(os.getcwd()))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "converter.settings")

import django
django.setup()


from converter.helpers import to_tag
from departments.models import Department
from topics.models import Topic

from pages.models import Page, DepartmentPage, PageTopic

import csv

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def to_int(value):
    """
    make sure the string works as an integer
    """
    return value.replace(',', '')

def read_csv(source_csv, dept_name, order='esd'):
    count = 0
    #with codecs.open(source_csv, 'rb', encoding='utf-8') as csvfile:
    with open(source_csv) as csvfile:
        reader = unicode_csv_reader(csvfile)

        #just print the first row:
        print '>, <'.join(reader.next())

        for row in reader:
            count += 1

            if order == 'esd':
                url = row[0]
                alias = row[2]
                #aka status/notes, or topic?
                tag = row[3]
                notes = row[4]
                title = row[5]
                page_views = to_int(row[6])
                page_views_unique = to_int(row[7])
                average_time = row[8]
                entrances = to_int(row[9])
                bounce_rate = row[10]
                exit_percent = row[11]
                section_id = row[12]
                categories = ','.join(row[13:])
            else:
                raise ValueError, "Unknown Order: %s" % order

            dept_options = Department.objects.filter(name=dept_name)
            if len(dept_options):
                department = dept_options[0]
            else:
                print "Be sure to import departments with 'make_departments.py'"
                raise ValueError, "Couldn't find department: %s" % dept_name

            #there is some filtering we can do here...
            tag = re.sub("DAM: keep", '', tag)
            tag = re.sub("DAM: Keep", '', tag)

            tags = []
            items = tag.split('/')
            for item in items:
                current = item.strip()
                if not current in tags:
                    tags.append(current)            

            default_topic = None
            for tag in tags:
                #aka status/notes, or topic?
                #tag = row[3]
                topic_options = Topic.objects.filter(name=tag)
                if len(topic_options):
                    topic = topic_options[0]
                elif tag:
                    topic = Topic()
                    #TODO: associate alias here?
                    topic.name = tag
                    topic.tag = to_tag(tag)
                else:
                    topic = None

                if topic:
                    #doing this again, for updates
                    #topic.name = tag
                    topic.save()
                    #print "Save topic here"
                    if not default_topic:
                        default_topic = topic

            page_options = Page.objects.filter(url=url)
            if len(page_options):
                page = page_options[0]
            elif url:
                #make a new one:
                page = Page()
                page.url = url

                page.alias = alias
                
                page.notes = notes
                page.title = title
                page.page_views = page_views
                page.page_views_unique = page_views_unique
                page.average_time = average_time
                page.entrances = entrances
                page.bounce_rate = bounce_rate
                page.exit_percent = exit_percent
                page.section_id = section_id
                page.categories = categories
                
            else:
                page = None

            if page:
                page.position = count
                page.default_topic = topic
                page.site = "bloomington.in.gov"
                page.save()
                #print "Save page here"

            department_page_options = DepartmentPage.objects.filter(page=page, department=department)
            if len(department_page_options):
                department_page = department_page_options[0]
            elif department and page:
                department_page = DepartmentPage()
                department_page.page = page
                department_page.department = department
            else:
                department_page = None

            if department_page:
                department_page.save()
                #print "Save department_page here"


            page_topic_options = PageTopic.objects.filter(page=page, topic=topic)
            if len(page_topic_options):
                page_topic = page_topic_options[0]
            elif page and topic:
                page_topic = PageTopic()
                page_topic.page = page
                page_topic.topic = topic
            else:
                #print "no page: %s -OR- no topic: %s" % (page, topic)
                page_topic = None

            if page_topic:
                page_topic.save()
                #print "Save page_topic here"
                
            

if __name__ == '__main__':
    read_csv('exports/esd.csv', "Economic & Sustainable Development")
                
