"""
Extract an IEX dataset from Redis (S3 support coming soon) and
load it into a ``pandas.DataFrame``

Supported environment variables:

::

    # verbose logging in this module
    export DEBUG_EXTRACT=1

    # verbose logging for just Redis operations in this module
    export DEBUG_REDIS_EXTRACT=1

    # verbose logging for just S3 operations in this module
    export DEBUG_S3_EXTRACT=1

    # to show debug, trace logging please export ``SHARED_LOG_CFG``
    # to a debug logger json file. To turn on debugging for this
    # library, you can export this variable to the repo's
    # included file with the command:
    export SHARED_LOG_CFG=/opt/sa/analysis_engine/log/debug-logging.json

"""

import copy
import analysis_engine.iex.consts as iex_consts
import analysis_engine.extract_utils as extract_utils
import spylunking.log.setup_logging as log_utils

log = log_utils.build_colorized_logger(name=__name__)


def extract_daily_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_daily_dataset

    Fetch the IEX daily data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_DAILY
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'daily' in req:
            req['redis_key'] = req['daily']
            req['s3_key'] = req['daily']
    # end of support for the get dataset dictionary

    log.debug(f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_daily_dataset


def extract_minute_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_minute_dataset

    Fetch the IEX minute intraday data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_MINUTE
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'minute' in work_dict:
            req['redis_key'] = req['minute']
            req['s3_key'] = req['minute']
    # end of support for the get dataset dictionary

    log.debug(
        f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_minute_dataset


def extract_quote_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_quote_dataset

    Fetch the IEX quote data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_QUOTE
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'quote' in work_dict:
            req['redis_key'] = req['quote']
            req['s3_key'] = req['quote']
    # end of support for the get dataset dictionary

    log.debug(f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_quote_dataset


def extract_stats_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_stats_dataset

    Fetch the IEX statistics data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_STATS
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'stats' in work_dict:
            req['redis_key'] = req['stats']
            req['s3_key'] = req['stats']
    # end of support for the get dataset dictionary

    log.debug(f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_stats_dataset


def extract_peers_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_peers_dataset

    Fetch the IEX peers data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_PEERS
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'peers' in work_dict:
            req['redis_key'] = req['peers']
            req['s3_key'] = req['peers']
    # end of support for the get dataset dictionary

    log.debug(f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_peers_dataset


def extract_news_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_news_dataset

    Fetch the IEX news data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_NEWS
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'news1' in work_dict:
            req['redis_key'] = req['news1']
            req['s3_key'] = req['news1']
    # end of support for the get dataset dictionary

    log.debug(f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_news_dataset


def extract_financials_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_financials_dataset

    Fetch the IEX financial data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_FINANCIALS
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'financials' in work_dict:
            req['redis_key'] = req['financials']
            req['s3_key'] = req['financials']
    # end of support for the get dataset dictionary

    log.debug(f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_financials_dataset


def extract_earnings_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_earnings_dataset

    Fetch the IEX earnings data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_EARNINGS
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'earnings' in work_dict:
            req['redis_key'] = req['earnings']
            req['s3_key'] = req['earnings']
    # end of support for the get dataset dictionary

    log.debug(f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_earnings_dataset


def extract_dividends_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_dividends_dataset

    Fetch the IEX dividends data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_DIVIDENDS
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'dividends' in work_dict:
            req['redis_key'] = req['dividends']
            req['s3_key'] = req['dividends']
    # end of support for the get dataset dictionary

    log.debug(f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_dividends_dataset


def extract_company_dataset(
        work_dict,
        scrub_mode='NO_SORT'):
    """extract_company_dataset

    Fetch the IEX company data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = iex_consts.DATAFEED_COMPANY
    df_str = iex_consts.get_datafeed_str(df_type=df_type)
    req = copy.deepcopy(work_dict)

    if 'redis_key' not in work_dict:
        # see if it's get dataset dictionary
        if 'company' in work_dict:
            req['redis_key'] = req['company']
            req['s3_key'] = req['company']
    # end of support for the get dataset dictionary

    log.debug(f'{label} - {df_str} - start')

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=req,
        scrub_mode=scrub_mode)
# end of extract_company_dataset
