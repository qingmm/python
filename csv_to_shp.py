#-*-coding:utf-8-*-
import shapefile as shp
import csv
import codecs
import os

def trans_point(folder, fn, idlng, idlat, delimiter=','):
    '''transfer a csv file to shapefile'''
    # create a point shapefile
    output_shp = shp.Writer(shp.POINT)
    # for every record there must be a corresponding geometry.
    output_shp.autoBalance = 1
    # create the field names and data type for each.you can omit fields here
    output_shp.field('longitude', 'F', 10, 8) # float
    output_shp.field('latitude', 'F', 10, 8) # float
    output_shp.field('theme', 'N')
    output_shp.field('category', 'N')
    output_shp.field('datetaken', 'C', 100) # string, max-length
    output_shp.field('url', 'C', 100) # string, max-length
    counter = 1 # count the features
    # access the CSV file
    with codecs.open(folder + fn, 'rb', 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        next(reader, None) # skip the header
        #loop through each of the rows and assign the attributes to variables
        for row in reader:
            lng= float(row[idlng])
            lat = float(row[idlat])
            theme = int(row[2])
            category = int(row[3])
            datetaken = row[4]
            url = row[5]
            output_shp.point(lng, lat) # create the point geometry
            output_shp.record(lng, lat, theme, category, datetaken, url) # add attribute data
            if counter % 10000 == 0:
                print "Feature " + str(counter) + " added to Shapefile."
            counter = counter + 1
    output_shp.save(folder + "%s.shp"%fn.split('.')[0]) # save the Shapefile

if __name__ == '__main__':
    folder = 'C:\Users\MaMQ\Desktop' + os.sep
    fn = 'scatter_honor_killing.csv'
    trans_point(folder, fn, 2, 3)

