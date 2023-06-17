#script to map avalanches from CAIC data

#import modules
# import directories
import arcpy
from arcpy import env
from arcpy.sa import *
import os
from collections import defaultdict
import datetime
print("arcpy imported")

# estabslish parameters
arcpy.env.workspace = "C:\\Users\\Emma Tyrrell\\Documents\\PSU_SDS\\THESIS_230226"
terrainDataFilesWorkspace = (arcpy.env.workspace + "\\Data\\TerrainData")
demFiles = (arcpy.env.workspace + "\\Data\\DEM")
projectBoundary = (arcpy.env.workspace + "\\Data\\StaticDataGDB.gdb\\ProjectBoundary")
AvyDataWorkspace = "C:\\Users\\Emma Tyrrell\\Documents\\PSU_SDS\\THESIS_230226\\Data\\AvyData"
Jan2022AvyTable = "C:\\Users\\Emma Tyrrell\\Documents\\PSU_SDS\\THESIS_230226\\Data\\AvyData\\2022\\CAICAvyExplorer_Jan22.csv"
xField = "X_Coord"
yField = "Y_Coord"
outAvyPointClass = (AvyDataWorkspace + "\\TestAvyPointClass.shp")
projectedAvyOutPointClass = (AvyDataWorkspace + "\\TestAvyPointClass_projected.shp")
avyPointClipped = (AvyDataWorkspace + "\\TestAvyPointClass_Clipped.shp")
arcpy.env.qualifiedFieldNames = False
GCSsr = arcpy.SpatialReference(4326)
PCSsr = arcpy.SpatialReference(6432)
print("parameters established")

# Prep shapefiles
try:
    # run tool for XY class
    arcpy.management.XYTableToPoint(Jan2022AvyTable, outAvyPointClass, xField, yField, "", GCSsr)
    print("point class created")

    #project class into proper cooridnate system
    arcpy.management.Project(outAvyPointClass, projectedAvyOutPointClass, PCSsr)
    print("coordinate system projected")

    fieldsPointClass = arcpy.ListFields(projectedAvyOutPointClass)
    for field in fieldsPointClass:
        print(field.name)

except Exception as ex:
    print(ex)

#clip to boundary
try:
    arcpy.analysis.Clip(projectedAvyOutPointClass, projectBoundary, avyPointClipped)
    print ("clipped avy feature")

except Exception as ex:
    print(ex)