# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 Scipp contributors (https://github.com/scipp)

from typing import NewType

import scipp as sc

from .io import (
    TIME_COORD_NAME,
    DarkCurrentImageStacks,
    OpenBeamImageStacks,
    SampleImageStacks,
)

AverageBackgroundPixelCounts = NewType("AverageBackgroundPixelCounts", sc.Variable)
"""~math:`D0 = mean(background)`."""
AverageSamplePixelCounts = NewType("AverageSamplePixelCounts", sc.Variable)
"""~math:`D = mean(sample)`."""
ScaleFactor = NewType("ScaleFactor", sc.Variable)
"""~math:`ScaleFactor = AverageBackgroundPixelCounts / AverageSamplePixelCounts`."""

OpenBeamImage = NewType("OpenBeamImage", sc.DataArray)
"""Open beam image. ~math:`average(open_beam)`."""
DarkCurrentImage = NewType("DarkCurrentImage", sc.DataArray)
"""Dark current image ~math:`average(dark_current)`."""
AveragedNonSampleImages = NewType("AveragedNonSampleImages", sc.DataArray)
"""Averaged open beam and dark current images."""
BackgroundImage = NewType("BackgroundImage", sc.DataArray)
"""Background image stack. ~math:`background = open_beam - dark_current`."""
CleansedSampleImages = NewType("CleansedSampleImages", sc.DataArray)
"""Sample image stack - dark current."""
NormalizedSampleImages = NewType("NormalizedSampleImages", sc.DataArray)
"""Normalized sample image stack.

~math:`normalized_sample = sample / background * DFactor`.
"""
GroupedSampleImages = NewType("GroupedSampleImages", sc.DataArray)
"""Grouped sample image stack by rotation angle."""


def average_open_beam_images(open_beam: OpenBeamImageStacks) -> OpenBeamImage:
    """Average the open beam image stack.

    .. math::

        OpenBeam = mean(open_beam, 'time')

    """
    return OpenBeamImage(sc.mean(open_beam, dim=TIME_COORD_NAME))


def average_dark_current_images(
    dark_current: DarkCurrentImageStacks,
) -> DarkCurrentImage:
    """Average the dark current image stack.

    .. math::

        DarkCurrent = mean(dark_current, 'time')

    """
    return DarkCurrentImage(sc.mean(dark_current, dim=TIME_COORD_NAME))


def calculate_white_beam_background(
    open_beam: OpenBeamImage, dark_current: DarkCurrentImage
) -> BackgroundImage:
    """Calculate the background image stack.

    We average the open beam and dark current image stack
    to create the single background image.

    .. math::

        Background = mean(OpenBeam, 'time') - mean(DarkCurrent, 'time')

    """
    return BackgroundImage(open_beam - dark_current)


def cleanse_sample_images(
    sample_images: SampleImageStacks, dark_current: DarkCurrentImage
) -> CleansedSampleImages:
    """Cleanse the sample image stack.

    We subtract the averaged dark current image from the sample image stack.

    .. math::

        CleansedSample_{i} = Sample_{i} - mean(DarkCurrent, dim='time')

        \\text{where } i \\text{ is an index of an image.}

    """
    return CleansedSampleImages(sample_images - dark_current)


def average_background_pixel_counts(
    background: BackgroundImage,
) -> AverageBackgroundPixelCounts:
    """Calculate the average background pixel counts."""
    return AverageBackgroundPixelCounts(background.data.mean())


def average_sample_pixel_counts(
    samples: CleansedSampleImages,
) -> AverageSamplePixelCounts:
    """Calculate the average sample pixel counts."""
    return AverageSamplePixelCounts(samples.data.mean())


def calculate_d_factor(
    average_bg: AverageBackgroundPixelCounts, average_sample: AverageSamplePixelCounts
) -> ScaleFactor:
    """Calculate the scale factor from average background and sample pixel counts.

    .. math::

            ScaleFactor = AverageBackgroundPixelCounts / AverageSamplePixelCounts

    """
    return ScaleFactor(average_bg / average_sample)


def normalize_sample_images(
    samples: CleansedSampleImages, factor: ScaleFactor, background: BackgroundImage
) -> NormalizedSampleImages:
    """Normalize the sample image stack.


    Default Normalization Formula
    -----------------------------

    .. math::

        NormalizedSample_{i} = CleansedSample_{i} / Background * DFactor


    .. math::

        ScaleFactor = AverageBackgroundPixelCounts / AverageSamplePixelCounts


    .. math::

        CleansedSample_{i} = Sample_{i} - mean(DarkCurrent, dim=\\text{\\'time\\'})

        \\text{where } i \\text{ is an index of an image.}

    """
    return NormalizedSampleImages((samples / background) * factor)
