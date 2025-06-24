# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Scipp contributors (https://github.com/scipp)

from typing import NewType

import scipp as sc

from ess.reduce.time_of_flight import pulse_index_from_event_time_zero

from .types import (
    DetectorData,
    PulsePeriod,
    PulseStride,
    PulseStrideOffset,
    RunType,
)

PulseIndex = NewType("PulseIndex", sc.Variable)


def compute_pulse_index(
    da: DetectorData[RunType],
    pulse_period: PulsePeriod,
    pulse_stride: PulseStride,
    pulse_stride_offset: PulseStrideOffset,
) -> PulseIndex:
    """"""
    pulse_index = pulse_index_from_event_time_zero(
        da=da, pulse_period=pulse_period, pulse_stride=pulse_stride
    )
    pulse_index += pulse_stride_offset
    pulse_index %= pulse_stride


def unfolded_pulse_skipping_data(
    da: DetectorData[RunType],
    pulse_index: PulseIndex,):
