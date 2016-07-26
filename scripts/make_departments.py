import os, sys, re
sys.path.append(os.path.dirname(os.getcwd()))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "converter.settings")

import django
django.setup()

from departments.models import Department
from converter.helpers import to_tag

print Department.objects.all()

import csv

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


def read_csv(source_csv):

    count = 0
    #with codecs.open(source_csv, 'rb', encoding='utf-8') as csvfile:
    with open(source_csv) as csvfile:
        reader = unicode_csv_reader(csvfile)

        #just print the first row:
        #print '>, <'.join(reader.next())

        for row in reader:
            count += 1
            dept_name = row[0]

            dept_options = Department.objects.filter(name=dept_name)
            if len(dept_options):
                department = dept_options[0]
            elif dept_name:
                #make a new one:
                department = Department()
                department.name = dept_name
            else:
                department = None

            if department:
                department.tag = to_tag(dept_name)
                department.save()

if __name__ == '__main__':
    read_csv('departments.csv')
                
