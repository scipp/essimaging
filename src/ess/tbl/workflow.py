# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Scipp contributors (https://github.com/scipp)
"""
Default parameters, providers and utility functions for the TBL workflow.
"""

import sciline
import scipp as sc

# from ess.reduce.workflow import register_workflow
# from ess.sans.io import read_xml_detector_masking
# from ess.sans.parameters import typical_outputs
from .conversion import providers as conversion_providers
from .nexus import LoadNeXusWorkflow
from .types import (
    DistanceResolution,
    LookupTableRelativeErrorThreshold,
    LtotalRange,
    Monitor1,
    NeXusMonitorName,
    PulsePeriod,
    PulseStride,
    PulseStrideOffset,
    TimeResolution,
)


def default_parameters() -> dict:
    return {
        NeXusMonitorName[Monitor1]: "monitor_1",
        PulsePeriod: 1.0 / sc.scalar(14.0, unit="Hz"),
        PulseStride: 1,
        PulseStrideOffset: None,
        LookupTableRelativeErrorThreshold: 1.0,
        LtotalRange: (sc.scalar(25.0, unit="m"), sc.scalar(35.0, unit="m")),
        DistanceResolution: sc.scalar(0.1, unit="m"),
        TimeResolution: sc.scalar(250.0, unit='us'),
    }


providers = (*conversion_providers,)


def TblWorkflow() -> sciline.Pipeline:
    """
    Workflow with default parameters for TBL.
    """
    workflow = LoadNeXusWorkflow()
    for provider in providers:
        workflow.insert(provider)
    for key, param in default_parameters().items():
        workflow[key] = param
    return workflow
