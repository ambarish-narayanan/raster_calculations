"""Demo percentile function."""
import sys
import os
import shutil
import logging
import multiprocessing

import pygeoprocessing
import raster_calculations_core
from osgeo import gdal
import taskgraph

gdal.SetCacheMax(2**30)

WORKSPACE_DIR = 'CNC_workspace'
NCPUS = -1
try:
    os.makedirs(WORKSPACE_DIR)
except OSError:
    pass

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '%(asctime)s (%(relativeCreated)d) %(levelname)s %(name)s'
        ' [%(funcName)s:%(lineno)d] %(message)s'),
    stream=sys.stdout)
LOGGER = logging.getLogger(__name__)


def main():
    """Write your expression here."""

    #path = r"C:\Users\Becky\Documents\raster_calculations\realized_flood_storage.tif"
    #percentile_working_dir = r"C:\Users\Becky\Documents\raster_calculations\flood_percentile_working_dir"
    path = r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_fwfish_distrib_catch_clamped_md5_54954ae73276d02e1d1551c9ac63298c.tif"
    percentile_working_dir = r"C:\Users\Becky\Documents\raster_calculations\percentile_working_dir"
    #makes a temporary directory because there's a shitton of rasters to find out the percentiles
    try:
        os.makedirs(percentile_working_dir)
    except OSError:
        pass
        #checks to see if the directory already exists, if it doesn't it makes it, if it does it doesn't do anything
    percentile_values_list = pygeoprocessing.raster_band_percentile(
        (path, 1), percentile_working_dir, [0, 0.01, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 96, 97, 98, 99, 99.9, 100])
    # (path,1) is indicating the first band in that "path" raster; the 2nd argument is the working dir; the third is the list of percentiles we want
    shutil.rmtree(percentile_working_dir)
    #this gets rid of that termporary directory
    print(percentile_values_list)

    return  # terminates at this point

# realized_reeftourism_Modelled_Total_Dollar_Value_of_Reef_Tourism_USD_per_km2_md5_171a993b8ff40d0447f343dd014c72e0
##0, 0.01, 1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 96, 97, 98, 99, 99.9, 100
# [0, 0,   0, 0, 0, 0, 0, 0,   0, 0,   0, 0,   0, 0,   0, 0,   0, 0,   0, 0,   2, 4,   6,  7, 9,  9,  10, 10, 10, 10,   10]
# realized_marinefish_watson_2015_catch_Ind_Non_Ind_Rprt_IUU_md5_61e08ed60006e9ad23b74bcd44c61548
# [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9]
# realized_moisturerecycling_nathab_md5_8fc0527f5aafb5947cf30debb50f825e
#[-46.6298828125, -37.2236328125, -2.6240234375, -0.7568359375, -0.2978515625, -0.0517578125, 0.1318359375, 0.8203125, 1.3134765625, 2.0888671875, 2.783203125, 3.7392578125, 5.5810546875, 8.171875, 11.2119140625, 14.50390625, 18.8642578125, 23.974609375, 30.931640625, 39.580078125, 48.5478515625, 58.1865234375, 69.0625, 86.9189453125, 114.5166015625, 121.6923828125, 132.30078125, 146.099609375, 169.0146484375, 239.0595703125, 285.03515625]
#mangrove_forest_value
# [0.09112019091844559, 0.1146746575832367, 0.36950379610061646, 0.5469441413879395, 0.6734423041343689, 0.7889978885650635, 0.9028277397155762, 1.2744618654251099, 1.5426571369171143, 1.7565761804580688, 1.9408801794052124, 2.094856023788452, 2.2336559295654297, 2.3777151107788086, 2.508002996444702, 2.6384236812591553, 2.749114990234375, 2.8938496112823486, 3.035269021987915, 3.1978647708892822, 3.4221363067626953, 3.744148015975952, 4.17542028427124, 4.662129878997803, 5.300693988800049, 5.447903156280518, 5.674015045166016, 6.024029731750488, 6.7951788902282715, 9.976946830749512, 21.237258911132812]
#realized_nitrogenretention_downstream_md5_82d4e57042482eb1b92d03c0d387f501
#        0th           25th    50th                 75th                   95th               99th                 100th
#  -680618713.5250311, 0.0, 13816.789725814846, 6,973,767.683561915, 79,365,495.3211188, 301,244,797.7473311, 38,828,470,375.24423
# realized_sedimentdeposition_downstream_md5_1613b12643898c1475c5ec3180836770
#        0th           1st  25th       50th          75th                   95th               99th                 100th
# [-2858.336473792897, 0.0, 0.0,        0.0,     402.0619507020006,    357620.664287882,   16,535,749.256560648,   6,597,664,634,840.14]
#realized_timber_md5_5154151ebe061cfa31af2c52595fa5f9
#        [0.0,        0.0,    0.0,       0.0,   0.012081013061106205,  0.31635093688964844, 0.7717771530151367,     1.0]
#realized_nwfp_md5_f1cce72af652fd16e25bfa34a6bddc63.tif
#        [0.0,        0.0,    0.0,       0.0,    0.001921603106893599, 0.10424786061048508, 0.548800528049469,      1.0]
#realized_grazing_md5_19085729ae358e0e8566676c5c7aae72.tif
#[0.0, 0.0, 0.0, 0.0, 0.0, 0.14973261952400208, 0.47111403942108154, 1.0]
#aggregate_realized_ES_score_nspwtg
#        [0.0,         0.0, 9.21e-05, 0.03501,     0.2486041,          1.0089664579947066, 1.708877055645255,       5.465055904557587]
# [0.0, 0.0, 0.00011389717641436895, 0.04634972283590727, 0.35257506411377726, 1.242382827708929, 2.0108227921844755, 5.953480030698451] (renorm, with Mark's layers normalized)
#realized_flood
# [0.0, 0.507854656299039, 35.99045191890391, 366.0255347248417, 1468.5788862469963, 3530.437843072411, 7069.98947579123, 12846.831757144722, 25987.817071338322, 63306.430552658385, 106175.18246477921, 153450.92538471072, 276336.67552793754, 1191192.2016361542]


## potential
# potential_wood_products.tif
# [0.0, 0.0, 0.0, 5.337533800359173e-13, 0.07046046108007431, 0.6822813153266907, 0.9767299890518188, 1.0]
# potential_grazing.tif
#[0.0, 0.0, 0.0, 0.0, 0.0, 0.3169699013233185, 0.6685281991958618, 1.0]
# potential_nitrogenretention.tif"
# [-860.8894653320312, 0.0, 0.0, 30.9406681060791, 44.82950973510742, 68.58059692382812, 122.13092803955078, 11120.1875]
# potential_sedimentdeposition.tif"
# [-0.0012096621794626117, 0.0, 0.0, 1.7197262422996573e-05, 0.007970078848302364, 1.40674889087677, 35.2034797668457, 1729475.125]
# aggregate_potential_ES_score_nspwpg (only 5 services; nothing to surrogate for non-wood foraged products)
# [8.223874317755279e-18, 0.06277088660611055, 0.31905198201749124, 0.43141886583982053, 0.5513050308982201, 0.7021776828519225, 0.8801414329582294, 1.0867488999270096, 1.3572950878165897, 1.5653558772021574, 2.14759821821794, 4.87844488615983]
# potential_flood_storage.tif
# [0.0, 0.005853109061717987, 0.015125198289752007, 0.019453035667538643, 0.025105200707912445, 0.03279130905866623, 0.04321467503905296, 0.054845262318849564, 0.06888996064662933, 0.08685627579689026, 0.10033410042524338, 0.11616448685526848, 0.2806900143623352]
# potential_moisture_recycling
# [0.012767312116920948, 13.39586067199707, 23.5416259765625, 34.7803955078125, 49.61043930053711, 67.15190887451172, 85.14018249511719, 107.3245849609375, 132.542724609375, 165.21200561523438, 198.92771911621094, 231.83872985839844, 400.93255615234375]




    poll_path = r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\potential_pollination_edge.tif"
    poll_working_dir = r"C:\Users\Becky\Documents\raster_calculations\poll_working_dir"
    try:
        os.makedirs(poll_working_dir)
    except OSError:
        pass
    poll_values_list = pygeoprocessing.raster_band_percentile(
        (poll_path, 1), poll_working_dir, [0, 1, 25, 50, 75, 95, 99, 100])
    shutil.rmtree(poll_working_dir)
    print("potential_pollination_edge.tif")
    print(poll_values_list)

    TASK_GRAPH.join()

    sed_path = r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\potential_sedimentdeposition.tif"
    sed_working_dir = r"C:\Users\Becky\Documents\raster_calculations\sed_working_dir"
    try:
        os.makedirs(sed_working_dir)
    except OSError:
        pass
    sed_values_list = pygeoprocessing.raster_band_percentile(
        (sed_path, 1), sed_working_dir, [0, 1, 25, 50, 75, 95, 99, 100])
    shutil.rmtree(sed_working_dir)

    print("potential_sedimentdeposition.tif")
    print(sed_values_list)

    TASK_GRAPH.join()

    nit_path = r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\potential_nitrogenretention.tif"
    nit_working_dir = r"C:\Users\Becky\Documents\raster_calculations\nit_working_dir"
    try:
        os.makedirs(nit_working_dir)
    except OSError:
        pass
    nit_values_list = pygeoprocessing.raster_band_percentile(
        (nit_path, 1), nit_working_dir, [0, 1, 25, 50, 75, 95, 99, 100])
    shutil.rmtree(nit_working_dir)

    print("potential_nitrogenretention.tif")
    print(nit_values_list)

    TASK_GRAPH.join()
    TASK_GRAPH.close()


    percentile_expression = {
        'expression': 'service / percentile(service, 100.0)',
        'symbol_to_path_map': {
            'service': r"C:\Users\rpsharp\Documents\bitbucket_repos\raster_calculations\lspop2017_md5_86d653478c1d99d4c6e271bad280637d.tif",
        },
        'target_nodata': -1,
        'target_raster_path': "normalized_service.tif",
    }
    raster_calculations_core.evaluate_calculation(
        percentile_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()




if __name__ == '__main__':
    TASK_GRAPH = taskgraph.TaskGraph(WORKSPACE_DIR, NCPUS, 5.0)
    main()
