"""SafeWISE-related definitions."""

# pylint: disable=unused-import,import-error,no-name-in-module,no-member
import os
import logging

import mnemonic
import semver
import safewiselib

from safewiselib.client import SafeWISEClient as Client
from safewiselib.exceptions import SafeWISEFailure, PinException
from safewiselib.transport import get_transport
from safewiselib.messages import IdentityType

from safewiselib.btc import get_public_node
from safewiselib.misc import sign_identity, get_ecdh_session_key

log = logging.getLogger(__name__)


def find_device():
    """Selects a transport based on `SafeWISE_PATH` environment variable.

    If unset, picks first connected device.
    """
    try:
        return get_transport(os.environ.get("SafeWISE_PATH"))
    except Exception as e:  # pylint: disable=broad-except
        log.debug("Failed to find a SafeWISE device: %s", e)
