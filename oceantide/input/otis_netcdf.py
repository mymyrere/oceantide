"""Read Otis netcdf file format."""
import os
import xarray as xr

from oceantide.core.otis import otis_to_oceantide, otis_filenames
from oceantide.tide import Tide


def read_otis_netcdf(filename=None, gfile=None, hfile=None, ufile=None):
    """Read Otis Netcdf file format.

    Args:
        - filename (str): Name of `Model_*` metadata file specifying other files to read.
        - gfile (str): Name of grid file to read, by default defined from `filename`.
        - hfile (str): Name of elevation file to read, by default defined from `filename`.
        - ufile (str): Name of currents file to read, by default defined from `filename`.

    Returns:
        - dset (Oceantide Dataset): Formatted dataset with the tide accessor.

    Note:
        - Otis data are usually provided in 4 separate files:
          - Meta file named as `Model_*` specifyig the 3 data files to read.
          - Grid file named as `grid*.nc` with grid information and model depths.
          - Elevation file named as `h*.*.nc` with elevation constituents data.
          - Transport file named as `uv.*.nc` with transport constituents data.
          The path of the three data files can be prescribed either by specifying the
          meta file path (`filename`) or by explicitly providing their path
          (`gfile`, `hfile` and `ufile`).

    """
    if filename is not None:
        _gfile, _hfile, _ufile = otis_filenames(filename)
    else:
        _gfile = _hfile = _ufile = None
        if not all([gfile, hfile, ufile]):
            raise ValueError(
                "Either specify `filename` or all of `gfile`, `hfile`, `ufile`."
            )

    gfile = gfile or _gfile
    hfile = hfile or _hfile
    ufile = ufile or _ufile

    dsg = xr.open_dataset(gfile, chunks={})
    dsh = xr.open_dataset(hfile, chunks={})
    dsu = xr.open_dataset(ufile, chunks={})

    dset = otis_to_oceantide(dsg, dsh, dsu)

    return dset


if __name__ == "__main__":


    hfile = "/data/tide/tpxo9v4a/netcdf/DATA/h_tpxo9.v4a.nc"
    ufile = "/data/tide/tpxo9v4a/netcdf/DATA/u_tpxo9.v4a.nc"
    gfile = "/data/tide/tpxo9v4a/netcdf/DATA/grid_tpxo9.v4a.nc"

    dset = read_otis_netcdf(gfile=gfile, hfile=hfile, ufile=ufile)
