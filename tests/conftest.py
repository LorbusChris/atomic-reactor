"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import print_function, unicode_literals

import pytest
import requests
import requests.exceptions
from tests.constants import LOCALHOST_REGISTRY_HTTP, DOCKER0_REGISTRY_HTTP, MOCK
from tests.util import uuid_value

from atomic_reactor.util import ImageName
from atomic_reactor.core import DockerTasker

if MOCK:
    from tests.docker_mock import mock_docker


@pytest.fixture()
def temp_image_name():
    return ImageName(repo=("atomic-reactor-tests-%s" % uuid_value()))


@pytest.fixture()
def is_registry_running():
    """
    is docker registry running (at {docker0,lo}:5000)?
    """
    try:
        lo_response = requests.get(LOCALHOST_REGISTRY_HTTP)
    except requests.exceptions.ConnectionError:
        return False
    if not lo_response.ok:
        return False
    try:
        lo_response = requests.get(DOCKER0_REGISTRY_HTTP)  # leap of faith
    except requests.exceptions.ConnectionError:
        return False
    if not lo_response.ok:
        return False
    return True


@pytest.fixture(scope="module")
def docker_tasker():
    if MOCK:
        mock_docker()
    return DockerTasker(retry_times=0)


@pytest.fixture(params=[True, False])
def reactor_config_map(request):
    return request.param


@pytest.fixture(params=[True, False])
def inspect_only(request):
    return request.param
