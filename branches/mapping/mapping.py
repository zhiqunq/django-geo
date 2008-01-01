"""Module for generating map widgets for HTML display."""

from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
import models as geo_models

class MapMarker(object):
	"""A map marker object."""
	latitude = 0.0
	longitude = 0.0
	label = None
	draggable=False
	
	def __init__(self, obj=None, **kwargs):
		for arg in kwargs:
			setattr(self, arg, kwargs[arg])
		if not obj is None:
			if (hasattr(obj, 'latitude') and hasattr(obj, 'longitude')):
				self.latitude, self.longitude = float(obj.latitude), float(obj.longitude)
			else:
				try:
					if type(obj[0]) in (float, int) and type(obj[1]) in (float, int):
						self.latitude, self.longitude = (float(o) for o in obj[0:2])
					else:
						raise TypeError
				except TypeError:
					raise TypeError('obj must be an object with both latitude and longitude attributes or an indexable object (0 and 1) that both are floats.')
			if hasattr(obj, 'name'):
				self.label = obj.name
		return super(MapMarker, self).__init__()
	
	def __str__(self):
		return 'Map Marker at (%s, %s)' % self.coords_tuple
	
	@property
	def coords(self):
		return {'latitude': self.latitude, 'longitude': self.longitude}
	
	@property
	def coords_tuple(self):
		return (self.latitude, self.longitude)
	
	def place(self, obj=None):
		"""Places the MapMarker onto the supplied place (obj). obj can be any object which has latitude and
		   longitude attributes or is indexable (0 and 1) to result in floats (latitude and longitude)."""
		if hasattr(obj, 'latitude') and hasattr(obj, 'longitude'):
			self.latitude, self.longitude = float(obj.latitude), float(obj.longitude)
			return
		else:
			try:
				if type(obj[0]) in (float, int) and type(obj[1]) in (float, int):
					self.latitude, self.longitude = (float(o) for o in obj[0:2])
					return
				else:
					raise TypeError
			except TypeError:
				raise TypeError('obj must be an object with both latitude and longitude attributes or an indexable object (0 and 1) that both are floats.')
	set_center = place # Consistency

class Widget(object):
	"""A map widget object."""
	center_latitude = 0.0
	center_longitude = 0.0
	bound = False
	bound_to = None
	markers = []
	
	def get_snippet(self):
		raise NotImplementedError
	
	@property
	def center(self):
		"""Returns a dictionary of the latitude and longitude for the center of this map widget."""
		return {'latitude': self.latitude, 'longitude': self.longitude}
	coords = center
	
	@property
	def center_tuple(self):
		"""Returns a 2-tuple of the latitude and longitude for the center of this map widget."""
		return (self.center_latitude, self.center_longitude)
	coords_tuple = tuple
	
	@property
	def latitude(self):
		return self.center_latitude
	
	@property
	def longitude(self):
		return self.center_longitude
	
	def bind(self, id, element='div'):
		"""Binds this map object to an element on a HTML page with a specified id.
		   Also takes an optional argument, element, that is a string of the bound element's
		   tag name (defaults to 'div')"""
		self.bound = True
		self.bound_to = '%s#%s' % (element, id)
	
	def for_location(self, location, add_marker=False, marker_label=None):
		"""Sets the necessary attributes to display the passed location."""
		self.set_center(location=location) # DRY - This will raise TypeError if location isn't a django-geo.models.Location instance.
		if add_marker:
			marker = self.add_marker(location=location, label=marker_label)
	
	def set_center(self, obj):
		"""Sets the center as the supplied place (obj). obj can be any object which has latitude and
		   longitude attributes or is indexable (0 and 1) to result in floats (latitude and longitude)."""
		if hasattr(obj, 'latitude') and hasattr(obj, 'longitude'):
			self.center_latitude, self.center_longitude = float(obj.latitude), float(obj.longitude)
			return
		else:
			try:
				if type(obj[0]) in (float, int) and type(obj[1]) in (float, int):
					self.center_latitude, self.center_longitude = (float(o) for o in obj[0:2])
					return
				else:
					raise TypeError
			except TypeError:
				raise TypeError('obj must be an object with both latitude and longitude attributes or an indexable object (0 and 1) that both are floats.')
	place = set_center # Consistency
	
	def add_marker(self, obj, **kwargs):
		"""Add a marker for the obj passed in. This can be any object which has either latitude
		   and longitude attributes or is indexable (0 and 1) to yield a latitude and longitude (
		   both must be floats -- for example a 2-tuple of latitude and longitude). Any other arguments
		   passed will be set as attributes of the resulting MapMarker."""
		if isinstance(obj, MapMarker):
			for argument in kwargs:
				setattr(obj, argument, kwargs[argument])
			self.markers.append(obj)
			return obj
		else:
			if hasattr(obj, 'latitude') and hasattr(obj, 'longitude'):
				marker = MapMarker(latitude=float(obj.latitude), longitude=float(obj.longitude), **kwargs)
				self.markers.append(marker)
				return marker
			else:
				try:
					if type(obj[0]) in (float, int) and type(obj[1]) in (float, int):
						marker = MapMarker(latitude=float(obj[0]), longitude=float(obj[1]), **kwargs)
						self.markers.append(marker)
						return marker
					else:
						raise TypeError
				except TypeError:
					raise TypeError('obj must be an object with both latitude and longitude attributes or an indexable object (0 and 1) that both are floats.')
	
	@property
	def head_tags(self):
		"""Subclasses should implement this to return the tags that should go in the <head> of a HTML page."""
		raise NotImplementedError
	
	def render_as_page(self, *args, **kwargs):
		"""Subclasses should implement this to render the widget to a full HTML page, taking an as_response
		   argument, which if True will cause the page to be rendered to a HttpResponse object rather than a
		   string."""
		raise NotImplementedError

class GoogleWidget(Widget):
	"""A Google Map Widget."""
	bound = False
	bound_to = None
	
	def __init__(self, api_key=None):
		self.api_key = api_key or settings.GEOCODING_KEYS['Google']
		return super(GoogleWidget, self).__init__()
	
	@property
	def head_tags(self):
		"""Returns the <script> tags which should go in the <head> of a HTML page."""
		return render_to_string('geo_templates/google_head_inclusion.html', {
			'object': self,
		})
	
	def render_page(self, as_response=False):
		"""Renders the widget to a full HTML page, consumed by the widget. If as_response
		   is True, then returns a HttpResponse of the rendered page."""
		if as_response:
			rendering_method = render_to_response
		else:
			rendering_method = render_to_string
		
		return rendering_method('geo_templates/google_widget_page.html', {
			'widget': self,
		})
	render_as_page = render_page # Backwards-compatibility
