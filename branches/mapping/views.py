"""Views for this application."""

from django.conf import settings
import mapping as geo_mapping
import models as geo_models
from django.http import Http404

def test_google_widget_page(request):
	"""Used to test the widget page renders correctly for a Google map widget, works only when
	   settings.DEBUG is True."""
	if not settings.DEBUG is True:
		raise Http404('This view is only available when settings.DEBUG is True.')
	else:
		return geo_mapping.GoogleWidget().render_as_page(as_response=True)
