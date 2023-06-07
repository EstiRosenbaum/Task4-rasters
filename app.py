from osgeo import gdal, osr
import numpy as np
import itertools as it

raster = gdal.Open('dir/1.jpg')
rasterSec = gdal.Open('dir/2.jpg')
rasterThr = gdal.Open('dir/3.jpg')
rasterFourth=gdal.Open('dir/4.jpg')

def exe_first_a(raster1, raster2):

    _, xres1, _, _, _, yres1 = raster1.GetGeoTransform()
    _, xres2, _, _, _, yres2 = raster2.GetGeoTransform()
    if (raster1.RasterXSize/(xres1*yres1)) > (raster2.RasterXSize/(xres2*yres2)):
        print(1)
    print(2)


def exe_first_b():

    gdal.Translate("dir/new20.jpg", "dir/2.jpg", projWin=(0, 0,
                   rasterSec.RasterXSize, rasterSec.RasterYSize/2))
    gdal.Translate("dir/new21.jpg", "dir/3.jpg", projWin=(0,
                   rasterThr.RasterYSize/2, rasterThr.RasterXSize, rasterThr.RasterYSize))

    p = gdal.Open('dir/new20.jpg')
    pp = gdal.Open('dir/new21.jpg')
    print(size(pp))
    gdal.Warp("halfRaster.tif", [pp, p], transformerOptions=[
              'SRC_METHOD=NO_GEOTRANSFORM', 'DST_METHOD=NO_GEOTRANSFORM'], width=2500, height=1488)


def create_mask(mask):
    format = 'GTiff'
    gdal.SetConfigOption('GDAL_TIFF_INTERNAL_MASK', 'YES')

    out_driver = gdal.GetDriverByName(format)
    outdataset = out_driver.Create(
        'new_mask.tif', rasterFourth.RasterXSize, rasterFourth.RasterYSize, rasterFourth.RasterCount)
    outdataset.CreateMaskBand(gdal.GMF_PER_DATASET)

    gt = rasterFourth.GetGeoTransform()
    outdataset.SetGeoTransform(gt)

    prj = rasterFourth.GetProjectionRef()
    outdataset.SetProjection(prj)   
    outband = outdataset.GetRasterBand(1)
    outmaskband = outband.GetMaskBand()
    outmaskband.WriteArray(mask)


def longest_streak(Input):
    Output = []
    temp = []
    last = -1
    index=[]
    # Iteration
    for elem in Input:
        if elem - last == 1:
            temp.append(last)
        else:
            temp.append(last)
            Output.append(temp)
            temp = []
        last = elem
        # index.append(elem[0])
        
    ans = []
    most = 0
    
    for elem in Output:
        if len(elem)> most:
            most = len(elem)
            ans = elem
    return([len(ans),ans[0]])
  
  
def exe_second():
   
  
    band1 = rasterFourth.GetRasterBand(1).ReadAsArray()
    band2 = rasterFourth.GetRasterBand(2).ReadAsArray()
    band3 = rasterFourth.GetRasterBand(3).ReadAsArray()
    arr=[]
    index=[]
    for i in range(len(band1)) :
        for j in range(len(band1[i])):
            if (band1[i][j] == band2[i][j] == band3[i][j]):
                band1[i][j]=1
                arr.append(j)
            else:
                band1[i][j]=0
        long=longest_streak(arr)        
        index.append([i,long])
    maxIndex=max(index,key=lambda x:x[1])    
    indexstart=maxIndex[1][1]
    i=100
    for i in range(maxIndex[1][0]):
        band1[maxIndex[0]][i+indexstart]=2
    create_mask(band1)
    # There is an option to use dstack but I don't know if it disrupts the bands----------------------- 
    # rgb_array = np.dstack([band1, band2, band3])
    # arr2=[]
    # for i in range(len(rgb_array)):
    #     for j in range(len(rgb_array[i])):
    #         b = list(rgb_array[i][j])
    #         if (all(element == b[0] for element in b)):              
    #             arr.append(j)
                # mat[i][j]=1
            # else:
                # mat[i][j]=0
    # matr=np.moveaxis(mat,0,0)
    #####(longest_contiguous = max([tuple(g) for _, g in it.groupby(arr)], key=len)
    # print(longest_contiguous) )#####
    # most_common = (set(arr), key=arr.count)
    # print(most_common)

           
def size(rastercheck):
    print("Driver: {}/{}".format(rastercheck.GetDriver().ShortName,
                                 rastercheck.GetDriver().LongName))
    print("Size is {} x {} x {}".format(rastercheck.RasterXSize,
                                        rastercheck.RasterYSize,
                                        rastercheck.RasterCount))
    print(rastercheck.RasterXSize*rastercheck.RasterYSize*rastercheck.RasterCount)

    print("Projection is {}".format(rastercheck.GetProjection()))
    geotransform = rastercheck.GetGeoTransform()
    if geotransform:
        print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
        print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
        print('hello')


exe_second()