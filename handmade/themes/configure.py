import os
from handmade.exceptions import ImproperlyConfigured
import kivy

from handmade.conf import settings
import importlib

try:
    theme_module = importlib.import_module(settings.THEME)
except ImportError:
    raise ImproperlyConfigured("Theme %s is not found" % settings.THEME)

kivy.kivy_data_dir = os.path.join(os.path.dirname(theme_module.__file__), 'data')
