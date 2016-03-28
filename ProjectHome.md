## Basic Info ##
In a nutshell, django-geo is a generic location-awareness application that you can use in your Django project. It allows you to easily geotag any object in your database, and is still under heavy development. Geocoding is performed in a fully automated and transparent fashion.

## API Reference ##
As django-geo is still under heavy development, I have taken the decision not to write any exhaustive API documentation at present. There are however, brief guides as to how to use django-geo in the documents linked in the links section of this page.

In addition to this, the code for django-geo is quite self-explanatory, and in most places there are [docstrings](http://www.python.org/dev/peps/pep-0257/) to explain a given class (or function, or whatever).

If there is something that you're stuck with however, [send me an email](mailto:oliver@obeattie.com) and I'll be happy to help.

## Download and Installation ##
The method most developers will prefer is to use Subversion to keep up to date with changes to django-geo. The SVN version will be the most current version of the code, and checkins are only done when the code is known to work fully.

**A word of warning, though; the SVN version _may_ include API changes with no forewarning for the coming months. If API stability is crucial, you must [download the latest release](http://code.google.com/p/django-geo/downloads/list).**

To check out the latest revision from SVN, enter the following command, which will download django-geo to a directory called geo:

```
svn checkout http://django-geo.googlecode.com/svn/trunk/ geo
```

Once downloaded, make sure the application is listed in your `INSTALLED_APPS` setting and on your `PYTHONPATH`.

## Contributing ##
If anyone does have any code they think would be useful to django-geo, please do [let me know](mailto:oliver@obeattie.com) and I'd love to make use of it in the project.

## Finally… ##
Enjoy!