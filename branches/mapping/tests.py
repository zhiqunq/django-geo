# -*- coding: utf-8 -*-
"""Unit testing for this module's fields and a subset of the model's functions.."""

from geopy import geocoders as geopy_geocoders, distance as geopy_distance
from django.test import TestCase
from django.db import models
from django.conf import settings
from fields import PickledObjectField
from test_assets import *
import models as geo_models
import mapping as geo_mapping

class PickledObjectFieldTests(TestCase):
	def setUp(self):
		self.testing_data = (
			{1:1, 2:4, 3:6, 4:8, 5:10},
			'Hello World',
			(1, 2, 3, 4, 5),
			[1, 2, 3, 4, 5],
			TestCustomDataType('Hello World'),
		)
		return super(PickledObjectFieldTests, self).setUp()
	
	def testDataIntegriry(self):
		"""Tests that data remains the same when saved to and fetched from the database."""
		for value in self.testing_data:
			model_test = TestingModel(pickle_field=value)
			model_test.save()
			model_test = TestingModel.objects.get(id__exact=model_test.id)
			self.assertEquals(value, model_test.pickle_field)
			model_test.delete()
	
	def testLookups(self):
		"""Tests that lookups can be performed on data once stored in the database."""
		for value in self.testing_data:
			model_test = TestingModel(pickle_field=value)
			model_test.save()
			self.assertEquals(value, TestingModel.objects.get(pickle_field__exact=value).pickle_field)

class GeocodingTest(TestCase):
	def __init__(self, *args, **kwargs):
		self.query = 'London, UK'
		self.location_object = geo_models.Location.objects.get_or_create(query=self.query)[0]
		return super(GeocodingTest, self).__init__(*args, **kwargs)
	
	def testGeocoding(self):
		returned_query, correct_coords = getattr(geopy_geocoders, settings.DEFAULT_GEOCODER)(settings.GEOCODING_KEYS[settings.DEFAULT_GEOCODER]).geocode(self.query)
		self.assertEquals(correct_coords, self.location_object.coords_tuple)
	
	def testModelFunctions(self):
		"""Tests that the various functions of the Location model perform as expected."""
		# Test the co-ordinate dictionary
		self.assertEquals({
			'latitude': self.location_object.latitude,
			'longitude': self.location_object.longitude,
		}, self.location_object.coords)
		# Test the co-ordinate two-tuple
		self.assertEquals((self.location_object.latitude, self.location_object.longitude), self.location_object.coords_tuple)
		# Test the name convenience function - we haven't set a friendly name so this should be equal
		# to the query
		self.assertEquals(self.query, self.location_object.query)
		# Test that the object is indexable (latitude and longitude)
		self.assertEquals(self.location_object[0], self.location_object.latitude)
		self.assertEquals(self.location_object[1], self.location_object.longitude)
		# Test the within_bounds function, with two locations known to be northwest and southeast of London
		self.location_object_nw = geo_models.Location.objects.get_or_create(query='Birmingham, UK')[0]
		self.location_object_se = geo_models.Location.objects.get_or_create(query='Brussels, Belgium')[0]
		self.assertEquals(self.location_object.within_bounds(north_west=self.location_object_nw, south_east=self.location_object_se), True)
		# Also test it with objects in opposite parts of the world
		self.assertEquals(True, geo_models.Location.objects.get_or_create(query='Sydney, Australia')[0].within_bounds(north_west=geo_models.Location.objects.get_or_create(query='Darwin, Australia')[0], south_east=geo_models.Location.objects.get_or_create(query='Wellington, New Zealand')[0]))
		# And finally test that it fails if given an area that is is not in
		self.assertEquals(False, self.location_object.within_bounds(north_west=geo_models.Location.objects.get_or_create(query='New York, NY, USA')[0], south_east=self.location_object_nw))

class MappingTest(TestCase):
	def __init__(self, *args, **kwargs):
		# Set a location_object (the mapping module can work with the Location and Point models)
		self.location_object = geo_models.Location.objects.get_or_create(query='London, UK')[0]
		return super(MappingTest, self).__init__(*args, **kwargs)
	
	def testMapMarker(self):
		"""Tests the MapMarker class behaves as expected."""
		# Test initialization works as expected
		# 1. With a django-geo.models.Location object
		marker = geo_mapping.MapMarker(self.location_object)
		self.assertEquals(self.location_object.latitude, marker.latitude)
		self.assertEquals(self.location_object.longitude, marker.longitude)
		# Also take this oppotunity to check that coords and coords_tuple both work correctly.
		self.assertEquals(self.location_object.coords, marker.coords)
		self.assertEquals(self.location_object.coords_tuple, marker.coords_tuple)
		del marker
		# 2. With a lat/long tuple
		marker = geo_mapping.MapMarker(self.location_object.coords_tuple)
		self.assertEquals(marker.latitude, self.location_object.latitude)
		self.assertEquals(marker.longitude, self.location_object.longitude)
	
	def testGoogleWidget(self):
		"""Tests the various methods of the Google widget class."""
		# Create a blank map widget
		map_widget = geo_mapping.GoogleWidget()
		# The API key is set correctly
		self.assertEquals(map_widget.api_key, settings.GEOCODING_KEYS['Google'])
	
	def testBaseWidget_setCenter(self):
		"""Tests the set_center method of the base Widget class."""
		map_widget = geo_mapping.Widget()
		# Test the set_center method works as expected
		# First, test the errors if given improper inputs
		self.assertRaises(TypeError, map_widget.set_center) # No inputs
		self.assertRaises(TypeError, map_widget.set_center, ('1.0', '2.0')) # Strings instead of float/int
		self.assertRaises(TypeError, map_widget.set_center, '1.0') # Non-indexable and no lat/long attributes
		# Now, test that the values are set correctly
		map_widget.set_center((20, 22)) # ...with a coords tuple of integers
		self.assertEquals(20, map_widget.center_latitude)
		self.assertEquals(22, map_widget.center_longitude)
		map_widget.set_center((20.20, 22.22)) # ...with a coords tuple of floats
		self.assertEquals(20.20, map_widget.center_latitude)
		self.assertEquals(22.22, map_widget.center_longitude)
		map_widget.set_center((30.30, 32)) # ...with a coords tuple of 1 float and 1 integer
		self.assertEquals(30.30, map_widget.center_latitude)
		self.assertEquals(32, map_widget.center_longitude)
		# By passing a Location object
		map_widget.set_center(self.location_object)
		self.assertEquals((map_widget.center_tuple), self.location_object.coords_tuple)
	
	def testBaseWidget_NotImplemented(self):
		"""Tests that various functions will raise a NotImplemented error if called on the base Widget class."""
		map_widget = geo_mapping.Widget()
		self.assertRaises(NotImplementedError, map_widget.render_as_page)
		try:
			# This is a property
			map_widget.head_tags
			self.fail('django-geo.mapping.Widget.head_tags did not raise a NotImplementedError')
		except NotImplementedError:
			pass
