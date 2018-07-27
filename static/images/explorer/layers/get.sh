
## wget -O arctic.xml       'http://map1.vis.earthdata.nasa.gov/wmts-arctic/1.0.0/WMTSCapabilities.xml'
## wget -O antarctic.xml    'http://map1.vis.earthdata.nasa.gov/wmts-antarctic/1.0.0/WMTSCapabilities.xml'
## wget -O planet.xml       'http://map1.vis.earthdata.nasa.gov/wmts-geo/1.0.0/WMTSCapabilities.xml'
## wget -O releasenotes.txt 'https://earthdata.nasa.gov/labs/worldview/release_notes.txt'

wget -O arctic-143.jpg   'http://map2.vis.earthdata.nasa.gov/imagegen/index.php?TIME=2013271&extent=-4194304,-4194304,4194304,4194304&epsg=3413&layers=MODIS_Terra_CorrectedReflectance_TrueColor&format=image/jpeg&width=160&height=160' 
wget -O arctic-367.jpg   'http://map2.vis.earthdata.nasa.gov/imagegen/index.php?TIME=2013271&extent=-4194304,-4194304,4194304,4194304&epsg=3413&layers=MODIS_Terra_CorrectedReflectance_Bands367&format=image/jpeg&width=160&height=160' 
wget -O arctic-721.jpg   'http://map2.vis.earthdata.nasa.gov/imagegen/index.php?TIME=2013271&extent=-4194304,-4194304,4194304,4194304&epsg=3413&layers=MODIS_Terra_CorrectedReflectance_Bands721&format=image/jpeg&width=160&height=160' 
wget -O arctic-mask.jpg  'http://map2.vis.earthdata.nasa.gov/imagegen/index.php?TIME=2013271&extent=-4194304,-4194304,4194304,4194304&epsg=3413&layers=land_water_map&format=image/jpeg&width=160&height=160' 
wget -O arctic-coast.jpg 'http://map2.vis.earthdata.nasa.gov/imagegen/index.php?TIME=2013271&extent=-4194304,-4194304,4194304,4194304&epsg=3413&layers=arctic_coastlines_3413&format=image/jpeg&width=160&height=160' 