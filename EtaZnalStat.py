# This script generates Zonal Statistics (temperature) from Raster file(MODIS)
# Author: Aashis Lamsal
# Supervisor: Ting-Wu

# Import System Modules
import sys,string,os,arcgisscripting,fnmatch
import psycopg2
from dbfpy import dbf
 

class EtaZnal:
    
    def __init__(self,etapath,znalshapepath,temppath,outputpath,logpath,znalcsvpath):

        self.etaPath=etapath
        self.znalshapePath=znalshapepath
        self.tempPath=temppath
        self.outputPath=outputpath
        self.logPath=logpath
        self.znalcsvPath=znalcsvpath
        self.dbhost='localhost'
        self.dbname='db_EastWeb'
        self.dbuser='postgres'
        self.dbpassword='eastweb1'

    '''Read already projected files date from log'''
    def ReadLog(self):
            logFilerd=open(self.logPath+"etaznal.txt",'r')
            logFilerd.seek(0)
            date=int(logFilerd.read())
            logFilerd.close()
            return date

    '''Write already project files date into log'''    
    def WriteLog(self,imagedate):
            logFilewrt=open(self.logPath+"etaznal.txt",'w')
            logFilewrt.seek(0)
            logFilewrt.write(imagedate) 
            logFilewrt.close()

    '''Connceting to the DB'''
    def InsertDB(self,year,day,zone,count,mean,stdev):
        
        #Define our connection string
        conn_string = "host="+self.dbhost+" dbname="+self.dbname+" user="+self.dbuser+" password="+self.dbpassword
        # print the connection string we will use to connect
        print "Connecting to database\n ->%s" % (conn_string)
        try:
                # get a connection, if a connect cannot be made an exception will be raised here
                conn = psycopg2.connect(conn_string)
                # conn.cursor will return a cursor object, you can use this cursor to perform queries
                cursor = conn.cursor()
                print "Connected!\n"
                cursor.execute("INSERT INTO tbl_eta(year,day,zone,count,mean,stdev) VALUES(%s,%s,%s,%s,%s,%s)",(year,day,zone,count,mean,stdev,))
                conn.commit()
                print "Sucessfully Inserted !!!"
                raise exit
        except:
                # Get the most recent exception
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                # Exit the script and print an error telling what happened.
                sys.exit("Database connection failed!\n ->%s" % (exceptionValue))

        
        
    def ComputeZnalStat(self):
        
        print "Please wait..........10 sec"

        # Create Geoprocessing object
        gp = arcgisscripting.create()

        # Check out any License
        gp.CheckOutExtension("spatial")

        # Overwriting the Output
        gp.OverwriteOutput =1

        #Location for ETa files
        masterFolder=self.etaPath

        #Define workspace dierctory
        gp.Workspace=masterFolder

        #Zonal shape file location
        zoneShape=self.znalshapePath

        #Zone Field
        zoneField="FIPS"

        #Zone output table location (temporary location but required)
        outputTable=self.tempPath+"temp.dbf"
        #Zone output dbf location
        
        outputDbf=self.tempPath

        #Raster summary Table Header
        tableHeader="YEAR, DATE, ZONE, COUNT, MEAN, STDEV\n"
        outTable=open(self.znalcsvPath,'a')
        outTable.write(tableHeader)

        ########### Generate Customized ETa Summary Table ################
        def CustomizeSummary(name,year,day):
            db = dbf.Dbf(name)
            for rec in db:
                zone= rec["FIPS"]
                count=rec["COUNT"]
                mean=rec["MEAN"]
                stddev=rec["STD"]
                outstr=year+","+day+","+str(zone)+","+str(count)+","+str(mean)+","+str(stddev)+"\n"
                #outTable.write(outstr)
                self.InsertDB(year,day,zone,count,mean,stddev)
                
                print outstr

        #Read ETa rasters
        etaList=list() # list to read eta files
        etaList=gp.ListRasters("*")
        eta=etaList.Next()

        # Generate ETa summary table
        while eta:
            if(int(self.ReadLog())<int(eta[3:10])):                    
                if fnmatch.fnmatch(eta,'ETa*'):
                    year=eta[3:7]
                    day=eta[7:10]

                    try:
                        gp.ZonalStatisticsAsTable_sa(zoneShape,zoneField,masterFolder+eta,outputTable,"DATA")
                    except Exception,e:
                        print "Could not compute ZonalStatisticsAsTable_sa:-: "+str(e)
                    gp.CopyRows_management(outputTable,outputDbf+eta+".dbf","")
                    CustomizeSummary(outputDbf+eta+".dbf",year,day)

                    self.WriteLog(str(eta[3:10]))

                    gp.delete_management(outputDbf+eta+".dbf")
                    gp.delete_management(outputTable)
            else:
                print "Zonal stat already computed for :-: "+str(eta)
            eta=etaList.Next()
        outTable.close()
      
if __name__=="__main__":

    #def __init__(self,etapath,shapepath,temppath,outputpath,logpath):
    ObjEtaZnal=EtaZnal("D:\\MODIS_ETa\\Data\\Eta\\","D:\\MODIS_LST_NDVI\\NGP_AEA\\NGP_AEA.shp","D:\\MODIS_ETa\\Output\\Temp\\","D:\\MODIS_ETa\\Output\\EtaZnal\\","D:\\MODIS_ETa\\Log\\","D:\\MODIS_ETa\\Output\\EtaZnal\\RasterSummary.csv")
    ObjEtaZnal.ComputeZnalStat()
    #ObjEtaZnal.InsertDB()
    

    
    
        
   
    

    
    


