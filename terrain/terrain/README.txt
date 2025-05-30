********** FILE FORMAT **********

The terrain data is stored in a .terrain file as plain text. Each file is structured as follows:

First Line: simply states "terrain", no quotes

Next Line: the size of the terrain "[# of columns] [# of rows]"

Next Line: number of water sources, X

Next X Lines: coordinate for each water source "[column index] [row index]"

Remaining Lines: a grid of float values for the range


********** ATTRIBUTION **********

The raw data for all maps, unless noted otherwise, comes from the National Oceanic
and Atmospheric Administration's website:

    https://maps.ngdc.noaa.gov/viewers/wcs-client/
    
We heard about this data source after reading Baker Franke's "Mountain Paths" Nifty assignment, available here:

    http://nifty.stanford.edu/2016/franke-mountain-paths/
    
The files Iceland.terrain, RioDeJaneiro.terrain, PearlRiverDelta.terrain, TeIkaAMaui.terrain,
VelingalaSenegal.terrain, and GulfOfGuinea.terrain were derived from the GEBCO 2020 Gridded Bathymetry Survey:

    https://download.gebco.net/
    
Attribution is as follows:

    "GEBCO Compilation Group (2020) GEBCO 2020 Grid (doi:10.5285/a29c5465-b138-234d-e053-6c86abc040b9)."

Some of the data were smoothed using a two-step grid refinement algorithm followed by a Gaussian blur.
    
The MarsOlmpusMons.terrain and MarsCraters.terrain files were created by former Winter 2020 CS106B student Varun
Shenoy based on the data available online at ASU (http://www.mars.asu.edu/data/mola_color/).

The file SouthWestNorway.terrain was created by former CS106B student Staale Jordan, based on data from the
Norwegian Mapping Agency website hoydedata.no.

The Guam.terrain file was based on data from the US Department of Agriclture's National Elevation Dataset:

    https://datagateway.nrcs.usda.gov/GDGOrder.aspx