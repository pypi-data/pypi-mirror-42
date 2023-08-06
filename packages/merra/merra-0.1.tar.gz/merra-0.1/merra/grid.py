# The MIT License (MIT)
#
# Copyright (c) 2019, TU Wien
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
The grid module implements the asymmetrical GMAO 0.5 x 0.625 grid
used in MERRA2 as a pygeogrids BasicGrid instance.
"""

import numpy as np
from pygeogrids.grids import BasicGrid


def create_merra_cell_grid():
    """
    Function creates the asymmetrical GMAO 0.5 x 0.625 grid as a
    BasicGrid instance.

    Returns
    -------
    BasicGrid instance
    """
    # define horizontal and vertical resolution of asymmetrical grid
    lon_res = 0.625
    lat_res = 0.5

    # create 361 (lat) x 576 (lon) mesh grid
    lon, lat = np.meshgrid(
        np.arange(-180, 180, lon_res),
        np.arange(-90, 90 + lat_res / 2, lat_res)
    )
    return BasicGrid(lon.flatten(), lat.flatten()).to_cell_grid(cellsize=5.)
