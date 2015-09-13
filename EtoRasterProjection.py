#Tools Description:Raster Projection
#Author:Ashis Lamsal
#Supervisor: Ting-Wu

# Import System Modules

import sys,string,os,arcgisscripting

# Create Geoprocessing object
gp = arcgisscripting.create()

# set Toolbox
gp.toolbox = "management"

# Check out any License
gp.CheckOutExtension("spatial")

# Overwriting the Output
gp.OverwriteOutput =1

#Define Workspace
gp.workspace="D:\\MODIS_ETa\\Output\\Eto_composite\\"

# Reading all raster files
rsList=gp.ListRasters("*")
rs=rsList.Next()

# Counter for Year day
i=1 

## Loop to read whole raster files
while rs:
    print rs
    
    #coordsys = "Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
    ## Assigning Projection types
    cs="C:\Program Files (x86)\\ArcGIS\\Coordinate Systems\\Projected Coordinate Systems\\Continental\\North America\\North America Albers Equal Area Conic.prj"
    coordsys="C:\\Program Files (x86)\\ArcGIS\\Coordinate Systems\\Geographic Coordinate Systems\\North America\North American Datum 1983.prj"
    print "Try to define Projections........."

    ## Define the projection and Coordinate System
    gp.defineprojection(rs, coordsys)

    print "Definition completed........."
    try:
        print "Try to reproject raster  "+rs

        ##Reproject Raster into Albers Equals Area
        #gp.ProjectRaster_management(InFileName, OutFileName, out_coordinate, resample, cell, geo_tran, reg_point, in_coordinate)
        gp.ProjectRaster_management(rs,"D:\\MODIS_ETa\\Output\\Eto_reproject\\"+"PrjETo2008"+str(i).zfill(3),cs,"NEAREST",1000,"","",coordsys)

        ##Increase counter by 8 day
        i=i+8
        print "Reprojection Done" 
        
    except:
        gp.GetMessages()
        raise "exit"
    rs=rsList.Next()
print "All the steps Completed Successfully"
   
   
