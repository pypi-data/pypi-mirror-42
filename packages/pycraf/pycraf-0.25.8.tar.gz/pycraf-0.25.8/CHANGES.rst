0.25.8 (2019-02-23)
=======================

Bugfixes
--------
- `pycraf.protection.ra769_limits` now returns an `astropy.table.QTable`
  instead of a `astropy.table.Table`. This ensures that in all
  circumstances one retrieves proper `astropy.units.Quantity` objects from
  the table. Previously, logarithmic units would not fully support this
  (although this was a just bug in `astropy`, which is now fixed). [#8]

0.25.7 (2018-11-24)
=======================

pycraf.antenna
^^^^^^^^^^^^^^
- Add k-factor to single element IMT2020 pattern in `pycraf.antenna`
  module. [#ef1c]
- Add antenna pattern function for IMT advance (LTE) basestation (sectorized,
  peak-side lobe, see ITU-R Rec. F.1336) to `pycraf.antenna` module. [#a4e1]

pycraf.srtm
^^^^^^^^^^^
- Various smaller improvements and bugfixes to SRTM querying.
  [#dcc5, #1950, #0c55]

Bugfixes
--------
- The `pycraf.geospatial` Gauss-Kruger test function revealed a problem with
  inconsistent results between new proj4 version (5.2.0) and older versions.
  At the moment, it is not clear, what's going on. The test cases have marked
  "xfail" for now. [#24e9]
- A sign was wrong in `pycraf.antenna` IMT2020 composite pattern. [#4164]

0.25.6 (2018-05-09)
=======================

pycraf.conversions
^^^^^^^^^^^^^^^^^^
- Add a function `protection.ra769_calculate_entry` that allows to calculate
  RA.769 thresholds for non-standard values (e.g., to query limits for
  RAS bands that are not included in the RA.769 tables).

Other
-----
- Update to newest version (v3.0) of Astropy helpers.

Bugfixes
--------
- Fixing a serious bug in the B03 tutorial notebook (reflections at wind
  turbines). Previously, we accounted twice for the distance when calculating
  the reflected power. As a result, the total received power at the
  RT is now much larger (though still smaller over direct path).


0.25.5 (2017-12-02)
=======================

pycraf.conversions
^^^^^^^^^^^^^^^^^^
- Add further utility routines to `pycraf.conversions` module, to compute
  antenna temperatures and sensitivities. [#8419]

pycraf.atm
^^^^^^^^^^^^^^^
- Add two new functions `atm.elevation_from_airmass` and `
  atm.airmass_from_elevation`, which use a better formula for small
  elevations (compared to the 1/sin(El) behavior). Furthermore,
  the elevation parameter in `atm.opacity_from_atten` and
  `atm.atten_from_opacity` has been made optional. If given, the
  airmass is corrected for (i.e., one works with zenith opacities). [#61e0]

API Changes
-----------
- The functions `pathprof.atten_path_fast` and `pathprof.atten_map_fast`
  now return dictionaries. This makes it easier to add new return values
  in the future (without API breaking). Three new parameters are returned
  for now: the type of path (Line-of-sight or Trans-horizon) and the
  distance of the horizon w.r.t. Tx/Rx.

Bugfixes
--------
- The solution to last exercise in the conversions tutorial notebook was
  wrong. (Thanks to A. Jessner for spotting this.)
- The `phi = 0`-singularity if using `do_bessel=True` in `antenna.ras_pattern`
  was not properly handled. [#5acf]

Other
-----
- Added some notebooks with exercises and solutions, as well as tutorial 03e.

0.25.4 (2017-09-21)
====================

New Features
------------

pycraf.antenna
^^^^^^^^^^^^^^^
- Add correlation-level parameter to `imt2020_composite_pattern`
  function. [#c57b]

pycraf.geometry
^^^^^^^^^^^^^^^
- Add various convenience functions to create 3D rotation matrices from
  rotation axis or Euler angles (and vice versa). Streamline the geometry
  subpackage to allow proper numpy broadcasting. [#c970]

pycraf.pathprof
^^^^^^^^^^^^^^^
- Add a method, `geoid_area` to calculate surface area on the WGS84
  ellipsoid. Only rectangular limits (absolute coordinates) are supported.
  This can be used to determine the area of SRTM pixels (in km^2). [#678f]
- Add a method `atten_path_fast`, which can be used to calculate attenuations
  for full paths very quickly (compared to the manual approach); also see
  tutorial notebooks. To produce the necessary aux-data dictionary,
  two functions are available: `height_path_data` and
  `height_path_data_generic`. To avoid confusion and to streamline
  everything, the function `heigth_profile_data` was renamed to
  `height_map_data`. [#9d6a]

pycraf.protection
^^^^^^^^^^^^^^^
- Add the possibility to generate VLBI threshold values in `ra769_limits`
  function, as contained in Table 3 of RA.769. Furthermore, it is now
  possible to specify the integration time to be used for the
  thresholds. [#8a15]

Documentation
-------------

- Add a notebook about how to tilt or rotate IMT2020 antenna patterns.
- Various updates.

Bugfixes
--------
- In `atm.atten_slant_annex1` the `obs_alt` parameter was not properly
  accounted for. This led to significant errors for high-altitude
  observers. [#f616]
- The function `imt2020_composite_pattern` in the antenna subpackage
  now allows better broadcasting of input arrays. Speed was also
  improved. [#b8ac, #1219]

0.25.3 (2017-08-09)
====================

New Features
------------

pycraf.geospatial
^^^^^^^^^^^^^^^^^
- This sub-package was heavily re-factored. One can now work with EPSG
  or ESRI codes (see docs) and there is a factory to produce arbitrary
  transforms, which come with correct docstrings and quantity/range
  checker (i.e, proper unit handling). Also, we finally made ITRF
  work. [#6892]

Bugfixes
--------
- Increase minimal numpy version to 1.11 to avoid build conflicts with
  MacOS and Windows wheels. The wheels are now built with this minimal
  numpy version (1.11) rather than the latest version. Users of wheels
  have to have at least the same numpy version as the one with which
  pycraf wheels were built. [#2139]


0.25.2 (2017-07-30)
====================

New Features
------------

pycraf.pathprof
^^^^^^^^^^^^^^^
- Add option `interp` to `SrtmConf` to allow different interpolation schemes
  for SRTM data. Currently, 'nearest', 'linear' (default), and 'spline' are
  supported. [#8b43]
- SRTM query functions now support numpy broadcasting. [#af45]

Bugfixes
--------

- SRTM-related plots in documentation were not rendered. [#ea01]
- Clutter loss for "CLUTTER.UNKNOWN" was buggy (must always be zero). [#a8b5]

0.25.1 (2017-07-28)
====================

Bugfixes
--------

- Tests now don't run any SRTM-data related function, only if the option
  `remote-data=any` is given (on CLI, within Python it is invoked with
  `pycraf.test(remote_data='any')`). Therefore, one doesn't need to
  manually download SRTM tiles beforehand anymore. [#eeab]


0.25.0 (2017-07-27)
====================


New Features
------------

General
^^^^^^^
- Minimize dependencies: for a some of `pycraf` sub-packages, do imports
  only on demand and not during pycraf importing. Examples are the
  `satellite` and `geospatial` sub-packages, that depend on `pyproj` and
  `sgp4`. Of course, to use these sub-packages, one has to install the
  necessary dependencies. [#8051]

- Tests that need to download data from the internet are now decorated with
  astropy's `@remote_data` decorator. If you want to run these tests, use::

      import pycraf
      pycraf.test(remote_data='any')

  or

      .. code-block:: bash
      python setup.py test --remote-data='any'

  otherwise, these will be skipped over. [#1444]

- MacOS tests finally work. [#239d]

pycraf.pathprof
^^^^^^^^^^^^^^^^^

- Much better handling of SRTM data was implemented. It is now possible to
  define the SRTM directory during run-time. Furthermore, one can have
  pycraf download missing tiles. For this a new `SrtmConf` manager was
  introduced. [#2d30, #01ba, #208c, #2b5d]

