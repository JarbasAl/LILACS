# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from lilacs.util.log import LOG


def create_echo_function(name, blacklist = None, whitelist=None):
    blacklist = blacklist or []

    def echo(message):
        """Listen for messages and echo them for logging"""
        try:
            js_msg = json.loads(message)

            if whitelist and js_msg.get("type") not in whitelist:
                return

            if blacklist and js_msg.get("type") in blacklist:
                return

        except Exception:
            pass
        LOG(name).debug(message)
    return echo