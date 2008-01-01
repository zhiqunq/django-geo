"""Extends geopy's geocoding capabilities to provide the ability to return a dictionary of attributes
   rather than a location and co-ordinate pair for a Yahoo! geocoder, if return_dict is specified upon
   initialization (as True, but defaults to False)."""

from geopy.geocoders import *
from elementtree import ElementTree
import re

NAMESPACE_RE = re.compile('^\{.+\}') # To remove xml namespace declarations from tag names, as they are unhelpful here.

class Yahoo(Yahoo):
	def __init__(self, app_id, format_string='%s', output_format='xml', return_dict=False):
		self.return_dict = bool(return_dict)
		return super(Yahoo, self).__init__(app_id, format_string, output_format)
	
	def parse_xml(self, page, *args, **kwargs):
		if not self.return_dict:
			return super(Yahoo, self).parse_xml(page, *args, **kwargs)
		else:
			if not isinstance(page, basestring):
				page = self._decode_page(page)
			
			tree = ElementTree.fromstring(page)
			self.element_tree = tree
			self.returned_attrs, self.returned_data, self.data_dict = {}, {}, {}
			
			for element in tree.getiterator():
				# Iterates over every element in the tree and adds it to the returned_data
				if element.text:
					element.text = str(element.text).strip()
					if element.text:
						self.returned_data.update({NAMESPACE_RE.sub('', str(element.tag.strip().lower())): str(element.text).strip()})
						self.data_dict.update({NAMESPACE_RE.sub('', str(element.tag.strip().lower())): str(element.text).strip()})
				# Also adds all element attributes to returned_attrs
				for attr in element.attrib:
					self.returned_attrs.update({attr:element.attrib[attr]})
			
			if 'latitude' in self.returned_data and 'longitude' in self.returned_data:
				from geopy import util
				self.returned_data.update({'coords': util.parse_geo('%s %s' %(self.returned_data['latitude'], self.returned_data['longitude']))})
				self.data_dict.update({'coords': self.returned_data['coords']})
			return {'data': self.returned_data, 'attrs': self.returned_attrs, 'element_tree': self.element_tree, 'raw_response': page}