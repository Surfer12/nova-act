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
from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime as dt
from typing import TypedDict, Dict, Any


@dataclass(frozen=True)
class ModelInput:
    """Input data for the model."""

    image: str
    prompt: str
    active_url: str
    legacy_workflow_run_id: str = ""


@dataclass(frozen=True)
class ModelOutput:
    """Output data from the model."""

    awl_raw_program: str


class RawMessageInput(TypedDict):
    """Type definition for input section of raw message."""

    screenshot: str
    prompt: str
    metadata: Dict[str, Any]
    agentRunCreate: Dict[str, str]


class RawMessageOutput(TypedDict):
    """Type definition for output section of raw message."""

    rawProgramBody: str


class RawMessage(TypedDict):
    """Type definition for the complete raw message."""

    input: RawMessageInput
    output: RawMessageOutput


@dataclass(frozen=True)
class Step:
    """
    Represents a single step in the Nova Act process.

    Attributes:
        model_input: Input data for the model
        model_output: Output data from the model
        observed_time: Timestamp when the step was observed
        rawMessage: Raw message data from the system
    """

    model_input: ModelInput
    model_output: ModelOutput
    observed_time: dt
    rawMessage: RawMessage

    @classmethod
    def from_message(cls, message: RawMessage) -> "Step":
        """
        Create a Step instance from a raw message.

        Args:
            message: Raw message containing input and output data

        Returns:
            Step: New Step instance with parsed data

        Raises:
            KeyError: If required fields are missing from the message
        """
        # Extract input data
        input_data = message.get("input", {})
        model_input = ModelInput(
            image=input_data.get("screenshot", ""),
            prompt=input_data.get("prompt", ""),
            active_url=input_data.get("metadata", {}).get("activeURL", ""),
            legacy_workflow_run_id=input_data.get("agentRunCreate", {}).get("workflowRunId", ""),
        )

        # Extract output data
        output_data = message.get("output", {})
        model_output = ModelOutput(awl_raw_program=output_data.get("rawProgramBody", ""))

        # Extract timing data
        observed_time = dt.fromtimestamp(time.time())

        return cls(
            model_input=model_input,
            model_output=model_output,
            observed_time=observed_time,
            rawMessage=message,
        )

    # Input validation
    def __post_init__(self) -> None:
        """
        Validate instance after creation.

        Raises:
            ValueError: If required fields are missing or invalid
        """
        if not self.model_input.image:
            raise ValueError("Screenshot is required")
        if not self.model_output.awl_raw_program:
            raise ValueError("Program body is required")
