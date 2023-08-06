# Copyright (C) 2018-2019 SignalFx, Inc. All rights reserved.
from .instrumentation import instrument, uninstrument, auto_instrument  # noqa
from .utils import create_tracer, trace  # noqa
from jaegermeister import create_tracer, auto_instrument
import os

# Django
default_app_config = 'jaegermeister.libraries.django_.apps.SignalFxConfig'  # noqa


def load(module):
    print('in load')
    if "SAGI_DEV" in os.environ:
        print("==========================================================")
        print("Loading...")
        print("==========================================================")


def boot_agent():
    tracer = create_tracer(
        config={
            'sampler': {
                'type': 'const',
                'param': 1
            },
            'logging': True,
            'jaeger_endpoint': 'http://localhost:14268/api/traces',
        },
        service_name='SFX_SAGI',
    )
    auto_instrument(tracer)


boot_agent()
