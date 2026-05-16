# Lab 5 scripts

import os
import sys

import wzm_lab5_functions as l5



#  Part 1:
#  Assign a variable to the Landsat file
landsat_path = r'C:/Users/wilbu/Documents/Spring 2026/GEOG 562/Lab5_2025/Landsat_image_corv.tif'
output_ndvi = r'C:/Users/wilbu/Documents/Spring 2026/GEOG 562/Lab5_2025/landsat_ndvi2.tif'

# Pass this to your new smart raster class
raster = l5.SmartRaster(landsat_path)

# Calculate NDVI and save to an output file
output_ndvi = raster.calculate_ndvi(red_index=3, nir_index=4, output_path=output_ndvi)
raster.close()
print(f'NDVI raster written to: {output_ndvi}')

  






# Part 2:
# Assign a variable to the parcels data shapefile path

import wzm_lab5_functions as l5
parcels_path = r'C:\Users\wilbu\Documents\Spring 2026\GEOG 562\Lab5_2025\Benton_County_TaxLots.shp'
output_parcels = r'C:\Users\wilbu\Documents\Spring 2026\GEOG 562\Lab5_2025\TaxLots_ndvi2.shp'

#  Pass this to your new smart vector class
vector = l5.SmartVector(parcels_path)

#  Calculate zonal statistics and add to the attribute table of the parcels shapefile
vector.calculate_zonal_stats(output_ndvi, band_index=1, output_column='avg_ndvi')
vector.save(output_parcels)
print(f'Parcel shapefile written to: {output_parcels}')

#  Part 3: Optional
#  Use matplotlib to make a map of your census tracts with the average NDVI values
if __name__ == '__main__':
    try:
        import matplotlib.pyplot as plt
        vector.gdf.plot(column='avg_ndvi', cmap='YlGn', legend=True, figsize=(12, 8))
        plt.title('Average NDVI by Parcel')
        plt.axis('off')
        plt.show()
    except ImportError:
        print('matplotlib is not installed; skipping optional map output.')









