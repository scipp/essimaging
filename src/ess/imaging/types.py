# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Scipp contributors (https://github.com/scipp)
from typing import NewType, TypeVar

import scipp as sc

from ess.reduce.nexus import types as reduce_t
from ess.reduce.time_of_flight import types as tof_t

ImageDetectorName = NewType('ImageDetectorName', str)
"""Histogram mode detector name."""

ImageKeyLogs = NewType('ImageKeyLogs', sc.DataArray)
"""Image key logs."""

RotationMotionSensorName = NewType('RotationMotionSensorName', str)
"""Rotation sensor name."""

RotationLogs = NewType('RotationLogs', sc.DataArray)
"""Rotation logs data."""

HistogramModeDetectorsPath = NewType('HistogramModeDetectorsPath', str)
"""Path to the histogram mode detectors in a nexus file."""

DEFAULT_HISTOGRAM_PATH = HistogramModeDetectorsPath(
    "/entry/instrument/histogram_mode_detectors"
)


# 1 TypeVars used to parametrize the generic parts of the workflow

BackgroundRun = reduce_t.BackgroundRun
DetectorData = reduce_t.DetectorData
DiskChoppers = reduce_t.DiskChoppers
EmptyBeamRun = reduce_t.EmptyBeamRun
Filename = reduce_t.Filename
SampleRun = reduce_t.SampleRun

DetectorLtotal = tof_t.DetectorLtotal
DetectorTofData = tof_t.DetectorTofData
PulsePeriod = tof_t.PulsePeriod
PulseStride = tof_t.PulseStride
PulseStrideOffset = tof_t.PulseStrideOffset
DistanceResolution = tof_t.DistanceResolution
TimeResolution = tof_t.TimeResolution
LtotalRange = tof_t.LtotalRange
LookupTableRelativeErrorThreshold = tof_t.LookupTableRelativeErrorThreshold
TimeOfFlightLookupTable = tof_t.TimeOfFlightLookupTable
SimulationResults = tof_t.SimulationResults

RunType = TypeVar("RunType", SampleRun, BackgroundRun, EmptyBeamRun)
