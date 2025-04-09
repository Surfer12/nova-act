# Copyright 2025 Amazon Inc

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Nova Act - A Python SDK for Amazon Nova Act."""

from nova_act.bridge import NovaActBridge
from nova_act.cli.main import load_config
from nova_act.nova_act import NovaAct
from nova_act.util.logging import setup_logging
from nova_act.types.act_errors import (
    ActAgentError,
    ActCanceledError,
    ActClientError,
    ActDispatchError,
    ActError,
    ActExceededMaxStepsError,
    ActGuardrailsError,
    ActInternalServerError,
    ActRateLimitExceededError,
    ActTimeoutError,
)
from nova_act.types.act_metadata import ActMetadata
from nova_act.types.act_result import ActResult
from nova_act.types.errors import (
    NovaActError,
    StartFailed,
    StopFailed,
    ValidationFailed,
)
from nova_act.util.jsonschema import BOOL_SCHEMA

__version__ = "0.1.0"
__all__ = [
    "NovaAct",
    "NovaActBridge",
    "ActError",
    "ActAgentError",
    "ActCanceledError",
    "ActClientError",
    "ActDispatchError",
    "ActExceededMaxStepsError",
    "ActGuardrailsError",
    "ActInternalServerError",
    "ActRateLimitExceededError",
    "ActTimeoutError",
    "ActMetadata",
    "ActResult",
    "NovaActError",
    "StartFailed",
    "StopFailed",
    "ValidationFailed",
    "BOOL_SCHEMA",
    "load_config",
    "setup_logging",
]
