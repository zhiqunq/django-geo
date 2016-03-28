# Introduction #

This document lists all major features that are planned for inclusion in a future release of django-geo. The features listed here may have already been included in an SVN revision -- if this is the case this will always be indicated.

# The List #

  * **`GeoField` model field** -- this will facilitate easy geotagging of any item, much in the way that [django-tagging](http://django-tagging.googlecode.com/) does with its `TagField`
  * **Easy retrieval of geotagged items** -- this should have been included from the very beginning, but the code originated from a project where this functionality was not needed and subsequently left-out due to time constraints. This will be implemented with _top priority_ and is currently in development (this will work using [Django's contenttypes framework](http://www.djangoproject.com/documentation/contenttypes/))
  * **Display of Locations on maps** -- to make the job of displaying the data on the front-end easier, Location objects should be allowed to be easily displayed on a variety of different map types (Google Maps, Yahoo! Maps, etc.)
  * **More unit tests** -- the current user tests are somewhat restricted. These will be expanded in time.

# Suggestions #

This list is by no means complete, and there are many smaller improvements that are planned for future release, which will be added to the list progressively. If you have a suggestion for a feature, please do [submit a ticket](http://code.google.com/p/django-geo/issues/entry) for `Type-Enhancement` and I'll certainly consider it for inclusion.