# -*- coding: utf8 -*-
import os
from self_update.sdk_version import get_version

package = 'missinglink'


def get_missinglink_cli_version():
    return os.environ.get('_ML_FORCE_VERSION', get_version(package))


def get_missinglink_package():
    return package
