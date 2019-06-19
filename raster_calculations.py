"""Process a raster calculator plain text expression."""
import time
import sys
import os
import logging
import urllib.request

from retrying import retry
from osgeo import osr
from osgeo import gdal
import pygeoprocessing
import taskgraph

WORKSPACE_DIR = 'raster_expression_workspace'
NCPUS = 4
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
    raster_calculation_list = [
        {
            'expression': 'mask(raster, 1, 2, 3, 4)',
            'symbol_to_path_map': {
                'raster': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/Globio4_landuse_10sec_2015_cropint_md5_7eefef29fbd0778857cb772c22b52ed9.tif'
            },
            'target_nodata': -1,
            'target_raster_path': 'outputs/landcover_mask.tif'
        },
        {
            'expression': '(load-export)/load',
            'symbol_to_path_map': {
                'load': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/worldclim_2015_modified_load_compressed_md5_e3072705a87b0db90e7620abbc0d75f1.tif',
                'export': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/worldclim_2015_n_export_compressed_md5_fa15687cc4d4fdc5e7a6351200873578.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "outputs/NC_nutrient_10s_cur.tif",
            'build_overview': True,
        },
        {
            'expression': '(load-export)/load',
            'symbol_to_path_map': {
                'load': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/worldclim_2050_ssp1_modified_load_compressed_md5_a5f1db75882a207636546af94cde6549.tif',
                'export': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/worldclim_2050_ssp1_n_export_compressed_md5_4b2b0a4ac6575fde5aca00de4f788494.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "outputs/NC_nutrient_10s_ssp1.tif",
            'build_overview': True,
        },
        {
            'expression': '(load-export)/load',
            'symbol_to_path_map': {
                'load': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/worldclim_2050_ssp3_modified_load_compressed_md5_e49e578ed025c0bc796e55b7f27f82f1.tif',
                'export': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/worldclim_2050_ssp3_n_export_compressed_md5_b5259ac0326b0dcef8a34f2086e8339b.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "outputs/NC_nutrient_10s_ssp3.tif",
            'build_overview': True,
        },
        {
            'expression': '(load-export)/load',
            'symbol_to_path_map': {
                'load': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/worldclim_2050_ssp5_modified_load_compressed_md5_7337576433238f70140be9ec5b588fd1.tif',
                'export': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/worldclim_2050_ssp5_n_export_compressed_md5_12b9caecc29058d39748e13bf5b5f150.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "outputs/NC_nutrient_10s_ssp5.tif",
            'build_overview': True,
        },
    ]

    for raster_calculation in raster_calculation_list:
        evaluate_calculation(raster_calculation)
        break

    TASK_GRAPH.join()
    return

    raster_calculation_from_local_files_list = [
        {
            'expression': '(future-current)/current',
            'symbol_to_path_map': {
                'future': 'outputs/NC_nutrient_10s_ssp1.tif',
                'current': 'outputs/NC_nutrient_10s_cur.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "outputs/NCchange_nutrient_10s_ssp1.tif",
            'build_overview': True,
        },
        {
            'expression': '(future-current)/current',
            'symbol_to_path_map': {
                'future': 'outputs/NC_nutrient_10s_ssp3.tif',
                'current': 'outputs/NC_nutrient_10s_cur.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "outputs/NCchange_nutrient_10s_ssp3.tif",
            'build_overview': True,
        },
        {
            'expression': '(future-current)/current',
            'symbol_to_path_map': {
                'future': 'outputs/NC_nutrient_10s_ssp5.tif',
                'current': 'outputs/NC_nutrient_10s_cur.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "outputs/NCchange_nutrient_10s_ssp5.tif",
            'build_overview': True,
        },
    ]

    for raster_calculation in raster_calculation_from_local_files_list:
        evaluate_calculation(raster_calculation)

    TASK_GRAPH.join()
    TASK_GRAPH.close()


def evaluate_calculation(args):
    """Evaluate raster calculator expression object.

    Parameters:
        args['expression'] (str): a symbolic arithmetic expression
            representing the desired calculation.
        args['symbol_to_path_map'] (dict): dictionary mapping symbols in
            `expression` to either raster paths or URLs. In the case of
            the latter, the file will be downloaded to a `WORKSPACE_DIR`
        args['target_nodata'] (numeric):
        args['target_raster_path'] (str):

    Returns:
        None.
    """
    args_copy = args.copy()
    expression_id = os.path.splitext(
        os.path.basename(args_copy['target_raster_path']))[0]
    expression_workspace_path = os.path.join(WORKSPACE_DIR, expression_id)
    expression_ecoshard_path = os.path.join(
        expression_workspace_path, 'ecoshard')
    try:
        os.makedirs(expression_ecoshard_path)
    except OSError:
        pass
    # process ecoshards if necessary
    symbol_to_path_band_map = {}
    download_task_list = []
    for symbol, path in args_copy['symbol_to_path_map'].items():
        if path.startswith('http://') or path.startswith('https://'):
            # download to local file
            local_path = os.path.join(
                expression_ecoshard_path,
                os.path.basename(path))
            download_task = TASK_GRAPH.add_task(
                func=download_url,
                args=(path, local_path),
                target_path_list=[local_path],
                task_name='download %s' % local_path)
            download_task_list.append(download_task)
            symbol_to_path_band_map[symbol] = (local_path, 1)
        else:
            symbol_to_path_band_map[symbol] = (path, 1)

    # this sets a common target sr, pixel size, and resample method .
    args_copy.update({
        'churn_dir': WORKSPACE_DIR,
        'symbol_to_path_band_map': symbol_to_path_band_map,
        })
    del args_copy['symbol_to_path_map']
    build_overview = (
        'build_overview' in args_copy and args_copy['build_overview'])
    if 'build_overview' in args_copy:
        del args_copy['build_overview']
    eval_raster_task = TASK_GRAPH.add_task(
        func=pygeoprocessing.evaluate_raster_calculator_expression,
        kwargs=args_copy,
        dependent_task_list=download_task_list,
        target_path_list=[args_copy['target_raster_path']],
        task_name='%s -> %s' % (
            args_copy['expression'],
            os.path.basename(args_copy['target_raster_path'])))
    if build_overview:
        overview_path = '%s.ovr' % (
            args_copy['target_raster_path'])
        TASK_GRAPH.add_task(
            func=build_overviews,
            args=(args_copy['target_raster_path'],),
            dependent_task_list=[eval_raster_task],
            target_path_list=[overview_path],
            task_name='overview for %s' % args_copy['target_raster_path'])


def build_overviews(raster_path):
    """Build external overviews for raster."""
    raster = gdal.Open(raster_path, gdal.OF_RASTER)
    min_dimension = min(raster.RasterXSize, raster.RasterYSize)
    overview_levels = []
    current_level = 2
    while True:
        if min_dimension // current_level == 0:
            break
        overview_levels.append(current_level)
        current_level *= 2

    gdal.SetConfigOption('COMPRESS_OVERVIEW', 'LZW')
    raster.BuildOverviews(
        'average', overview_levels, callback=_make_logger_callback(
            'build overview for ' + os.path.basename(raster_path) +
            '%.2f%% complete'))


def _make_logger_callback(message):
    """Build a timed logger callback that prints ``message`` replaced.

    Parameters:
        message (string): a string that expects 2 placement %% variables,
            first for % complete from ``df_complete``, second from
            ``p_progress_arg[0]``.

    Returns:
        Function with signature:
            logger_callback(df_complete, psz_message, p_progress_arg)

    """
    def logger_callback(df_complete, _, p_progress_arg):
        """Argument names come from the GDAL API for callbacks."""
        try:
            current_time = time.time()
            if ((current_time - logger_callback.last_time) > 5.0 or
                    (df_complete == 1.0 and
                     logger_callback.total_time >= 5.0)):
                # In some multiprocess applications I was encountering a
                # ``p_progress_arg`` of None. This is unexpected and I suspect
                # was an issue for some kind of GDAL race condition. So I'm
                # guarding against it here and reporting an appropriate log
                # if it occurs.
                if p_progress_arg:
                    LOGGER.info(message, df_complete * 100, p_progress_arg[0])
                else:
                    LOGGER.info(
                        'p_progress_arg is None df_complete: %s, message: %s',
                        df_complete, message)
                logger_callback.last_time = current_time
                logger_callback.total_time += current_time
        except AttributeError:
            logger_callback.last_time = time.time()
            logger_callback.total_time = 0.0

    return logger_callback


def _preprocess_rasters(
        base_raster_path_list, churn_dir, target_sr_wkt=None,
        target_pixel_size=None, resample_method='near'):
    """Process base raster path list so it can be used in raster calcs.

    Parameters:
        base_raster_path_list (list): list of arbitrary rasters.
        churn_dir (str): path to a directory that can be used to write
            temporary files that could be used later for
            caching/reproducibility.
        target_sr_wkt (string): if not None, this is the desired
            projection of the target rasters in Well Known Text format. If
            None and all symbol rasters have the same projection, that
            projection will be used. Otherwise a ValueError is raised
            indicating that the rasters are in different projections with
            no guidance to resolve.
        target_pixel_size (tuple): It not None, desired output target pixel
            size. A ValueError is raised if symbol rasters are different
            pixel sizes and this value is None.
        resample_method (str): if the symbol rasters need to be resized for
            any reason, this method is used. The value can be one of:
            "near|bilinear|cubic|cubicspline|lanczos|average|mode|max".

    Returns:
        list of raster paths that can be used in raster calcs, note this may
        be the original list of rasters or they may have been created by
        this call.

    """
    resample_inputs = False

    base_info_list = [
        pygeoprocessing.get_raster_info(path)
        for path in base_raster_path_list]
    base_projection_list = [info['projection'] for info in base_info_list]
    base_pixel_list = [info['pixel_size'] for info in base_info_list]
    base_raster_shape_list = [info['raster_size'] for info in base_info_list]

    target_sr_wkt = None
    if len(set(base_projection_list)) != 1:
        if target_sr_wkt is not None:
            raise ValueError(
                "Projections of base rasters are not equal and there "
                "is no `target_sr_wkt` defined.\nprojection list: %s",
                str(base_projection_list))
        else:
            LOGGER.info('projections are different')
            target_srs = osr.SpatialReference()
            target_srs.ImportFromWkt(target_sr_wkt)
            target_sr_wkt = target_srs.ExportToWkt()
            resample_inputs = True

    if len(set(base_pixel_list)) != 1:
        if target_pixel_size is None:
            raise ValueError(
                "base and reference pixel sizes are different and no target "
                "is defined.\nbase pixel sizes: %s", str(base_pixel_list))
        LOGGER.info('pixel sizes are different')
        resample_inputs = True
    else:
        # else use the pixel size they all have
        target_pixel_size = base_pixel_list[0]

    if len(set(base_raster_shape_list)) != 1:
        LOGGER.info('raster shapes different')
        resample_inputs = True

    if resample_inputs:
        LOGGER.info("need to align/reproject inputs to apply calculation")
        try:
            os.makedirs(churn_dir)
        except OSError:
            LOGGER.debug('churn dir %s already exists', churn_dir)

        operand_raster_path_list = [
            os.path.join(churn_dir, os.path.basename(path)) for path in
            base_raster_path_list]
        pygeoprocessing.align_and_resize_raster_stack(
            base_raster_path_list, operand_raster_path_list,
            [resample_method]*len(base_raster_path_list),
            target_pixel_size, 'intersection', target_sr_wkt=target_sr_wkt)
        return operand_raster_path_list
    else:
        return base_raster_path_list


@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def download_url(url, target_path, skip_if_target_exists=False):
    """Download `url` to `target_path`."""
    try:
        if skip_if_target_exists and os.path.exists(target_path):
            return
        with open(target_path, 'wb') as target_file:
            with urllib.request.urlopen(url) as url_stream:
                meta = url_stream.info()
                file_size = int(meta["Content-Length"])
                LOGGER.info(
                    "Downloading: %s Bytes: %s" % (target_path, file_size))

                downloaded_so_far = 0
                block_size = 2**20
                while True:
                    data_buffer = url_stream.read(block_size)
                    if not data_buffer:
                        break
                    downloaded_so_far += len(data_buffer)
                    target_file.write(data_buffer)
                    status = r"%10d  [%3.2f%%]" % (
                        downloaded_so_far, downloaded_so_far * 100. /
                        file_size)
                    LOGGER.info(status)
    except:
        LOGGER.exception("Exception encountered, trying again.")
        raise


if __name__ == '__main__':
    TASK_GRAPH = taskgraph.TaskGraph(WORKSPACE_DIR, NCPUS, 5.0)
    main()
