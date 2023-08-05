from typing import Optional

import numpy as np
from skimage.morphology import ball, disk, white_tophat

from starfish.imagestack.imagestack import ImageStack
from starfish.util import click
from ._base import FilterAlgorithmBase
from .util import determine_axes_to_group_by


class WhiteTophat(FilterAlgorithmBase):
    """
    Performs "white top hat" filtering of an image to enhance spots. "White top hat filtering"
    finds spots that are both smaller and brighter than their surroundings.

    See Also
    --------
    https://en.wikipedia.org/wiki/Top-hat_transform
    """

    def __init__(self, masking_radius: int, is_volume: bool=False) -> None:
        """
        Instance of a white top hat morphological masking filter which masks objects larger
        than `masking_radius`

        Parameters
        ----------
        masking_radius : int
            radius of the morphological masking structure in pixels
        is_volume : int
            If True, 3d (z, y, x) volumes will be filtered, otherwise, filter 2d tiles
            independently.

        """
        self.masking_radius = masking_radius
        self.is_volume = is_volume

    _DEFAULT_TESTING_PARAMETERS = {"masking_radius": 3}

    def _white_tophat(self, image: np.ndarray) -> np.ndarray:
        if self.is_volume:
            structuring_element = ball(self.masking_radius)
        else:
            structuring_element = disk(self.masking_radius)
        return white_tophat(image, selem=structuring_element)

    def run(
            self, stack: ImageStack, in_place: bool=False, verbose: bool=False,
            n_processes: Optional[int]=None
    ) -> ImageStack:
        """Perform filtering of an image stack

        Parameters
        ----------
        stack : ImageStack
            Stack to be filtered.
        in_place : bool
            if True, process ImageStack in-place, otherwise return a new stack
        verbose : bool
            If True, report on the percentage completed (default = False) during processing
        n_processes : Optional[int]
            Number of parallel processes to devote to calculating the filter

        Returns
        -------
        ImageStack :
            If in-place is False, return the results of filter as a new stack.  Otherwise return the
            original stack.

        """
        group_by = determine_axes_to_group_by(self.is_volume)
        result = stack.apply(
            self._white_tophat,
            group_by=group_by, verbose=verbose, in_place=in_place, n_processes=n_processes
        )
        return result

    @staticmethod
    @click.command("WhiteTophat")
    @click.option(
        "--masking-radius", default=15, type=int,
        help="diameter of morphological masking disk in pixels")
    @click.option(  # FIXME: was this intentionally missed?
        "--is-volume", is_flag=True, help="filter 3D volumes")
    @click.pass_context
    def _cli(ctx, masking_radius, is_volume):
        ctx.obj["component"]._cli_run(ctx, WhiteTophat(masking_radius, is_volume))
