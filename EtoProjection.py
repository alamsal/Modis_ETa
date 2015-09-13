#Tools Description:Raster Projection
#Author:Ashis Lamsal
#Supervisor: Ting-Wu

# Import System Modules

import sys,string,os,arcgisscripting

class EtoReprojection:
    def __init__(self,rasterfile,yearday):

        self.rasterFile=rasterfile
        self.yearDay=yearday
        print "upto here -->1"


    def Reproject(self):

        print "upto here -->2"
        
        rs=self.rasterFile
        print rs
        # Create Geoprocessing object
        GP = arcgisscripting.create()

        # set Toolbox
        GP.toolbox = "management"

        # Check out any License
        GP.CheckOutExtension("spatial")

        # Overwriting the Output
        GP.OverwriteOutput =1

        # Define Workspace
        GP.workspace="D:\\MODIS_ETa\\Output\\Eto_composite\\"

        # coordsys = "Coordinate Systems/Geographic Coordinate Systems/North America/North American Datum 1983.prj"
        # Assigning Projection types
        cs="C:\\Program Files (x86)\\ArcGIS\\Coordinate Systems\\Projected Coordinate Systems\\Continental\\North America\\North America Albers Equal Area Conic.prj"
        coordsys="C:\\Program Files (x86)\\ArcGIS\\Coordinate Systems\\Geographic Coordinate Systems\\North America\North American Datum 1983.prj"

        print "Try to define Projections........."

            ## Define the projection and Coordinate System
        GP.defineprojection(rs, coordsys)

        print "Definition completed........."
        try:
            print "Try to reproject raster  "+rs

            ##Reproject Raster into Albers Equals Area
            #GP.ProjectRaster_management(InFileName, OutFileName, out_coordinate, resample, cell, geo_tran, reg_point, in_coordinate)
            GP.ProjectRaster_management(rs,"D:\\MODIS_ETa\\Output\\Eto_reproject\\"+"PrjETo2008"+str(self.yearDay).zfill(3),cs,"NEAREST",1000,"","",coordsys)
            print "Reprojection Done" 
            
        except:
            GP.GetMessages()
            raise "exit"
        
##if __name__=="__main__":
##    ObjEtoReprojection=EtoReprojection(r"D:\MODIS_ETa\Output\Eto_composite\eto2008009","9")
##    ObjEtoReprojection.Reproject()
    
    
    

           
           
