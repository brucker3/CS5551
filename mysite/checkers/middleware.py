# -*- coding: utf-8 -*

#@inspired by: https://djangosnippets.org/snippets/1723/
#@inspired by: https://gist.github.com/DrMartiner/ee93bd6fe1af4875f086f8396d13acd8
# @ inspired by: https://docs.djangoproject.com/en/3.1/
from __future__ import unicode_literals

import logging
from django.conf import settings
from importlib import import_module

engine = import_module(settings.SESSION_ENGINE)
SessionStore = engine.SessionStore

logger = logging.getLogger('django.request')

#@inspired by: https://djangosnippets.org/snippets/1723/
#@inspired by: https://gist.github.com/DrMartiner/ee93bd6fe1af4875f086f8396d13acd8
# @ inspired by: https://docs.djangoproject.com/en/3.1/

class AnonymousSessionMiddleware(object):
    def process_request(self, request):
        # type: (request) -> None
        if not request.user.is_authenticated() and not request.session.session_key:
            request.session = SessionStore()
            request.session.create()

            function_name = settings.get('ANONYMOUS_SESSION_PROCESS_FUNCTION')
            if function_name:
                msg = None
                try:
                    function = __import__(function_name)
                    if callable(function):
                        function()
                    else:
                        msg = '"{}" is not callable'.format(function_name)
                        logger.warn(msg)
                except ImportError:
                    msg = 'Can not import "{}"'.format(function_name)
                    logger.warn(msg)
                except Exception as e:
                    msg = 'Error at processing Anonymous request'
                    logger.warn(msg, exc_info=True)


def process_anonymous_session(request):
    # type: (request) -> None
    pass
