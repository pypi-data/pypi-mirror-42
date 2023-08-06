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
The reshuffle module implements a command line interface to convert the MERRA2
data into a time series format using the repurpose package.

USAGE in terminal:
reshuffle.py [-h] [--imgbuffer IMGBUFFER]
                    dataset_root timeseries_root start end parameters
                    [parameters ...]
"""

import os
import sys
import argparse

from datetime import datetime

from repurpose.img2ts import Img2Ts
from merra.interface import MerraImageStack
from pygeogrids import BasicGrid


def mkdate(date_string):
    """
    Define date/month string

    Parameters
    ----------
    date_string : string
        Date information in the filename

    Returns
    -------
    datetime : datetime.datetime object
        datetime object created from a string

    """
    if len(date_string) == 10:
        return datetime.strptime(date_string, '%Y-%m-%d')
    if len(date_string) == 16:
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M')


def reshuffle(in_path,
              out_path,
              start_date,
              end_date,
              parameters,
              temporal_sampling=6,
              img_buffer=50):
    """
    Reshuffle method applied to MERRA2 data.

    Parameters
    ----------
    in_path: string
        input path where merra2 data was downloaded
    out_path : string
        Output path.
    start_date : datetime
        Start date.
    end_date : datetime
        End date.
    parameters: list
        parameters to read and convert
    temporal_sampling: int in range [1, 24]
            Get an image every n hours where n=temporal_sampling. For example:
            if 1: return hourly sampled data -> hourly sampling
            if 6: return an image every 6 hours -> 6 hourly sampling
            if 24: return the 00:30 image of each day -> daily sampling
    img_buffer: int, optional
        How many images to read at once before writing the time series.
    """

    # define input dataset
    # the img_bulk class in img2ts iterates through every nth
    # timestamp as specified by temporal_sampling
    input_dataset = MerraImageStack(data_path=in_path,
                                    parameter=parameters,
                                    temporal_sampling=temporal_sampling,
                                    array_1d=True)
    product = 'MERRA2_hourly'

    # create out_path directory if it does not exist yet
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    # set global attribute
    global_attributes = {'product': product}

    # get ts attributes from fist day of data
    data = input_dataset.read(start_date)
    ts_attributes = data.metadata
    # define grid
    grid = BasicGrid(data.lon, data.lat)

    # define reshuffler
    reshuffler = Img2Ts(input_dataset=input_dataset,
                        outputpath=out_path,
                        startdate=start_date,
                        enddate=end_date,
                        input_grid=grid,
                        imgbuffer=img_buffer,
                        cellsize_lat=5.0,
                        cellsize_lon=6.25,
                        global_attr=global_attributes,
                        zlib=True,
                        unlim_chunksize=1000,
                        ts_attributes=ts_attributes)
    reshuffler.calc()


def parse_args(args):
    """
    Parse command line parameters for conversion from image to timeseries

    Parameters
    ----------
    args : list of strings
        command line parameters as list of strings

    Returns
    -------
    args : object
        command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Convert MERRA2 images to time series format.")
    parser.add_argument(
        "dataset_root",
        help='Root of local filesystem where the data is stored.')
    parser.add_argument(
        "timeseries_root",
        help='Root of local filesystem where the timeseries will be stored.')
    parser.add_argument("start", type=mkdate, help=(
        "Startdate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."))
    parser.add_argument("end", type=mkdate, help=(
        "Enddate. Either in format YYYY-MM-DD or YYYY-MM-DDTHH:MM."))
    parser.add_argument("parameters", metavar="parameters",
                        nargs="+",
                        help=("Parameters to download in numerical format."))

    parser.add_argument("--temporal_sampling", type=int, default=6,
                        help=(
                            "The temporal sampling of the output time series."
                            "Integers between 1 (1-hourly resolution) and 24"
                            "(daily resolution) are possible."))

    parser.add_argument(
        "--imgbuffer",
        type=int,
        default=50,
        help=(
            "How many images to read at once. Bigger numbers make the "
            "conversion faster but consume more memory."))

    args = parser.parse_args(args)
    # set defaults that can not be handled by argparse
    print("Converting data from {} to {} into folder {}.".format(
        args.start.isoformat(), args.end.isoformat(), args.timeseries_root))
    return args


def main(args):
    # parse command line arguments
    args = parse_args(args)

    # hand over to reshuffle routine
    reshuffle(args.dataset_root,
              args.timeseries_root,
              args.start,
              args.end,
              args.parameters,
              temporal_sampling=args.temporal_sampling,
              img_buffer=args.imgbuffer)


def run():
    main(sys.argv[1:])


if __name__ == '__main__':
    run()
