# -*- coding: utf-8 -*-
"""Assets for use in this module's unit tests."""

from django.db import models
from fields import PickledObjectField

class TestingModel(models.Model):
	pickle_field = PickledObjectField()

class TestCustomDataType(str):
	pass