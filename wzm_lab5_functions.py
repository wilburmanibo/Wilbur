#####################
# Block 1:  Import the packages you'll need
# 
# 

import os, sys
import numpy as np
import rasterio
from rasterio.features import geometry_mask
import geopandas as gpd






##################
# Block 2: 
# set the working directory to the directory where the data are

# Change this to the directory where your data are

data_dir = "C:/Users/wilbu/Documents/Spring 2026/GEOG 562/Lab5_2025/pythoncode"
os.chdir(data_dir)
print(os.getcwd())


##################
# Block 3: 
#   Set up a new smart raster class using rasterio  
#    that will have a method called "calculate_ndvi"


class SmartRaster:
    def __init__(self, raster_path):
        self.raster_path = raster_path
        self.dataset = rasterio.open(self.raster_path)
        self.meta = self.dataset.meta.copy()

    def calculate_ndvi(self, red_index=3, nir_index=4, output_path=None):
        """Calculate NDVI from a multiband raster and write the result to a new file."""
        red = self.dataset.read(red_index).astype('float32')
        nir = self.dataset.read(nir_index).astype('float32')

        np.seterr(divide='ignore', invalid='ignore')
        ndvi = (nir - red) / (nir + red)
        ndvi = np.where(np.isfinite(ndvi), ndvi, np.nan).astype('float32')

        profile = self.meta.copy()
        profile.update(count=1, dtype='float32', nodata=np.nan, compress='lzw')

        if output_path is None:
            base, _ = os.path.splitext(self.raster_path)
            output_path = f"{base}_ndvi.tif"

        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except PermissionError:
                base, ext = os.path.splitext(output_path)
                output_path = f"{base}_ndvi_{os.getpid()}{ext}"

        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(ndvi, 1)

        return output_path

    def close(self):
        self.dataset.close()


##################
# Block 4: 
#   Set up a new smart vector class using geopandas
#    that will have a method similar to what did in lab 4
#    to calculate the zonal statistics for a raster
#    and add them as a column to the attribute table of the vector


class SmartVector:
    def __init__(self, vector_path):
        self.vector_path = vector_path
        self.gdf = gpd.read_file(self.vector_path)

    def calculate_zonal_stats(self, raster_path, band_index=1, output_column='mean_ndvi'):
        """Calculate mean raster values inside each polygon and add them to the GeoDataFrame."""
        with rasterio.open(raster_path) as src:
            if self.gdf.crs is not None and src.crs is not None and self.gdf.crs != src.crs:
                self.gdf = self.gdf.to_crs(src.crs)

            raster = src.read(band_index)
            nodata = src.nodata
            results = []

            for geom in self.gdf.geometry:
                if geom is None or geom.is_empty:
                    results.append(np.nan)
                    continue

                try:
                    mask = geometry_mask(
                        [geom],
                        transform=src.transform,
                        invert=True,
                        out_shape=(src.height, src.width),
                        all_touched=False,
                    )
                except Exception:
                    results.append(np.nan)
                    continue

                values = raster[mask]
                if nodata is not None:
                    values = values[values != nodata]
                values = values[np.isfinite(values)]

                if values.size == 0:
                    results.append(np.nan)
                else:
                    results.append(float(np.nanmean(values)))

        self.gdf[output_column] = results
        return self.gdf

    def save(self, output_path):
        self.gdf.to_file(output_path)







