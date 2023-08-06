#
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import functools
import os

import pytest

from safewiselib import debuglink, log
from safewiselib.debuglink import SafeWISEClientDebugLink
from safewiselib.device import wipe as wipe_device
from safewiselib.transport import enumerate_devices, get_transport

SafeWISE_VERSION = None


def get_device():
    path = os.environ.get("SafeWISE_PATH")
    if path:
        return get_transport(path)
    else:
        devices = enumerate_devices()
        for device in devices:
            if hasattr(device, "find_debug"):
                return device
        raise RuntimeError("No debuggable device found")


def device_version():
    device = get_device()
    if not device:
        raise RuntimeError()
    client = SafeWISEClientDebugLink(device)
    if client.features.model == "T":
        return 2
    else:
        return 1


@pytest.fixture(scope="function")
def client():
    wirelink = get_device()
    client = SafeWISEClientDebugLink(wirelink)
    wipe_device(client)

    client.open()
    yield client
    client.close()


def setup_client(mnemonic=None, pin="", passphrase=False):
    if mnemonic is None:
        mnemonic = " ".join(["all"] * 12)
    if pin is True:
        pin = "1234"

    def client_decorator(function):
        @functools.wraps(function)
        def wrapper(client, *args, **kwargs):
            debuglink.load_device_by_mnemonic(
                client,
                mnemonic=mnemonic,
                pin=pin,
                passphrase_protection=passphrase,
                label="test",
                language="english",
            )
            return function(client, *args, **kwargs)

        return wrapper

    return client_decorator


def pytest_configure(config):
    global SafeWISE_VERSION
    SafeWISE_VERSION = device_version()

    if config.getoption("verbose"):
        log.enable_debug_output()


def pytest_addoption(parser):
    parser.addini(
        "run_xfail",
        "List of markers that will run even tests that are marked as xfail",
        "args",
        [],
    )


def pytest_runtest_setup(item):
    """
    Called for each test item (class, individual tests).

    Performs custom processing, mainly useful for safewise CI testing:
    * 'skip_t2' tests are skipped on T2 and 'skip_t1' tests are skipped on T1.
    * no test should have both skips at the same time
    * allows to 'runxfail' tests specified by 'run_xfail' in pytest.ini
    """
    if item.get_marker("skip_t1") and item.get_marker("skip_t2"):
        pytest.fail("Don't skip tests for both safewises!")

    if item.get_marker("skip_t2") and SafeWISE_VERSION == 2:
        pytest.skip("Test excluded on SafeWISE T")
    if item.get_marker("skip_t1") and SafeWISE_VERSION == 1:
        pytest.skip("Test excluded on SafeWISE")

    xfail = item.get_marker("xfail")
    runxfail_markers = item.config.getini("run_xfail")
    run_xfail = any(item.get_marker(marker) for marker in runxfail_markers)
    if xfail and run_xfail:
        # Deep hack: pytest's private _evalxfail helper determines whether the test should xfail or not.
        # The helper caches its result even before this hook runs.
        # Here we force-set the result to False, meaning "test does NOT xfail, run as normal"
        # IOW, this is basically per-item "--runxfail"
        item._evalxfail.result = False
