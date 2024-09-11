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


def _mean_all_dims(data: sc.Variable) -> sc.Variable:
    """Calculate the mean of all dimensions one by one to avoid overflow."""
    if data.shape == ():  # scalar
        return data
    return _mean_all_dims(data.mean(dim=data.dims[0]))


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

    Any value less than 1 is replaced with 1.

    .. math::

        Background = mean(OpenBeam, 'time') - mean(DarkCurrent, 'time')

    """
    diff = open_beam - dark_current
    threshold = sc.scalar(1.0, unit=diff.unit)
    diff.data = sc.where(diff.data < threshold, threshold, diff.data)
    return BackgroundImage(diff)


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
    sample_images: CleansedSampleImages, dark_current: DarkCurrentImage
) -> AverageSamplePixelCounts:
    """Calculate the average sample pixel counts.

    Note that we calculate the mean of sample images and dark current images
    first and subtract them afterwards,
    instead of using the subtracted image stack directly.
    This is for performance reasons, as the integer operation is faster than
    the floating point operation.

    Also, we don't calculate ``mean(sample_images)`` at once
    since it is a large array and it may cause memory issues.

    There was an example of 361 images of 2048x2048 pixels with 32-bit integer data
    exceeded the limit of the maximum integer so the average calculation failed
    and returned negative values.
    """
    return AverageSamplePixelCounts(
        _mean_all_dims(sample_images.data) - dark_current.data.mean()
    )


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


    Raises
    ------
    ValueError
        If the scale factor is negative.
        It is for the safety of the calculation on short data type.
        Depending on how you calculate the scale factor,
        the operation might fail and return negative values.

    """
    if factor < 0:
        raise ValueError(f"Scale factor must be positive, but got {factor}.")
    return NormalizedSampleImages(samples / (background * factor))
