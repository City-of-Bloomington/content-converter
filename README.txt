Site Migration
====================

Site Migration is a web based application to help track the migration of content from one content management system to another. This is useful for non-automated site migrations, when an audit of all content is desired before giving it a place in the new system. 

As content grows over time in a content management system, documents get forgotten and abandoned. It can be difficult to know if content is no longer relevant and out of date, or if it is a viable resource that just doesn't change frequently. Traffic statistics and analytics can help give clues in this regard, but they're not a silver bullet. They won't help with duplicated content, or designing a better content architecture. Eventually it's a good idea to manually review, but that can be a daunting process with a large enough set of data.

Site Migration helps track this process. An initial scan of the source yields the list of pages to work on. These can then be prioritized, commented upon, and linked up with their destination. 


Installation
------------------

Install Django, and install a database.

Clone this repository and edit converter/settings.py to reflect your database configuration. 

After initializing the database with:

    python manage.py migrate

Then need to import initial data via scripts directory:

    cd scripts
    python make_departments.py 





This application is written in Python on top of the Django framework, but the content management system being migrated from or to does not have to integrate with python directly. This system works with meta data or direct web requests. 
