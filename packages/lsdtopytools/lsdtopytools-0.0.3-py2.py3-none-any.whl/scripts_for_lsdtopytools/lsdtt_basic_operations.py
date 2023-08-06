#!/usr/bin/env python
"""
Command-line tool to control the concavity constraining tools
Mudd et al., 2018
So far mostly testing purposes
B.G.
"""
from lsdtopytools import LSDDEM, raster_loader as rl # I am telling python I will need this module to run.
from lsdtopytools import argparser_debug as AGPD # I am telling python I will need this module to run.
from lsdtopytools import quickplot as qp, quickplot_movern as qmn # We will need the plotting routines
import time as clock # Basic benchmarking
import sys # manage the argv

def PreProcess():
	# Here are the different parameters and their default value fr this script
	default_param = AGPD.get_common_default_param()
	default_param["breach"] = False
	default_param["fill"] = False
	default_param["min_slope"] = 0.0001



	default_param = AGPD.ingest_param(default_param, sys.argv)

	if(default_param["help"] or len(sys.argv)==1):
		print("""
			This command-line tool provides basic Preprocessing functions for a raster.
			Breaching is achieved running https://doi.org/10.1002/hyp.10648 algorithm (Lindsay2016), with an implementation from RICHDEM
			Filling is from Wang and liu 2006. I think MDH implemented the code.
			It also "clean" the raster and tidy the nodata in it.
			To use, run the script with relevant options, for example:
			-> filling and breaching
				lsdtt-depressions file=myraster.tif fill breach 0.00001 

			option available:
				file: name of the raster (file=name.tif)
				path: path to the file (default = current folder)
				breach: want to breach?
				fill: want to fill?
				min_slope: imply a min slope for filling

			""")
		quit()


	print("Welcome to the command-line tool to .")
	print("Let me first load the raster ...")
	mydem = LSDDEM(file_name = default_param["file"], path=default_param["path"], already_preprocessed = False, verbose = False)
	print("Got it. Now dealing with the depressions ...")
	mydem.PreProcessing(filling = default_param["fill"], carving = default_param["breach"], minimum_slope_for_filling = default_param["min_slope"]) # Unecessary if already preprocessed of course.

	print("Saving the raster! same name basically, but with _PP at the end")
	rl.save_raster(mydem.cppdem.get_PP_raster(),mydem.x_min,mydem.x_max,mydem.y_max,mydem.y_min,mydem.resolution,mydem.crs,mydem.path+mydem.prefix + "_PP.tif", fmt = 'GTIFF')

def Polyfit_Metrics():

	# Here are the different parameters and their default value fr this script
	default_param = AGPD.get_common_default_param()
	default_param["breach"] = False
	default_param["fill"] = False
	default_param["window_radius"] = 30

	default_param["average_elevation"] = False
	default_param["slope"] = False
	default_param["aspect"] = False
	default_param["curvature"] = False
	default_param["planform_curvature"] = False
	default_param["profile_curvature"] = False
	default_param["tangential_curvature"] = False
	default_param["TSP"] = False



	default_param = AGPD.ingest_param(default_param, sys.argv)

	if(default_param["help"] or len(sys.argv)==1):
		print("""
			This command-line tool provides basic Preprocessing functions for a raster.
			Breaching is achieved running https://doi.org/10.1002/hyp.10648 algorithm (Lindsay2016), with an implementation from RICHDEM
			Filling is from Wang and liu 2006. I think MDH implemented the code.
			It also "clean" the raster and tidy the nodata in it.
			To use, run the script with relevant options, for example:
			-> filling and breaching
				lsdtt-depressions file=myraster.tif fill breach 0.00001 

			option available:
				file: name of the raster (file=name.tif)
				path: path to the file (default = current folder)
				TODO
			""")
		quit()


	print("Welcome to the command-line tool to .")
	print("Let me first load the raster ...")
	mydem = LSDDEM(file_name = default_param["file"], path=default_param["path"], already_preprocessed = True, verbose = False)

	mydem.get_polyfit_metrics(window_radius = default_param["window_radius"], average_elevation = default_param["average_elevation"], slope = default_param["slope"], aspect = default_param["aspect"], curvature = default_param["curvature"], planform_curvature = default_param["planform_curvature"], profile_curvature = default_param["profile_curvature"], tangential_curvature = default_param["tangential_curvature"], TSP = default_param["TSP"], save_to_rast = True)






