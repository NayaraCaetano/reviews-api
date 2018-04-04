from .base import *


DEBUG = False

# Remove browsable API enabled in base
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.MultiPartRenderer',
)

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
)
