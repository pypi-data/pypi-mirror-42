"""
Dataset Extraction API
"""

import os
import json
import analysis_engine.consts as ae_consts
import analysis_engine.utils as ae_utils
import analysis_engine.iex.extract_df_from_redis as iex_extract_utils
import analysis_engine.yahoo.extract_df_from_redis as yahoo_extract_utils
import analysis_engine.td.extract_df_from_redis as td_extract_utils
import analysis_engine.api_requests as api_requests
import spylunking.log.setup_logging as log_utils

log = log_utils.build_colorized_logger(name=__name__)


def extract(
        ticker=None,
        tickers=None,
        use_key=None,
        extract_mode='all',
        iex_datasets=None,
        redis_enabled=True,
        redis_address=None,
        redis_db=None,
        redis_password=None,
        redis_expire=None,
        s3_enabled=True,
        s3_address=None,
        s3_bucket=None,
        s3_access_key=None,
        s3_secret_key=None,
        s3_region_name=None,
        s3_secure=False,
        celery_disabled=True,
        broker_url=None,
        result_backend=None,
        label=None,
        verbose=False):
    """extract

    Extract all cached datasets for a stock ``ticker`` or
    a list of ``tickers`` and returns a dictionary. Please
    make sure the datasets are already cached in Redis
    before running this method. If not please refer to
    the ``analysis_engine.fetch.fetch`` function
    to prepare the datasets on your environment.

    Python example:

    .. code-block:: python

        from analysis_engine.extract import extract
        d = extract(ticker='NFLX')
        print(d)
        for k in d['NFLX']:
            print(f'dataset key: {k}')


    This was created for reducing the amount of typying in
    Jupyter notebooks. It can be set up for use with a
    distributed engine as well with the optional arguments
    depending on your connectitivty requirements.

    .. note:: Please ensure Redis and Minio are running
              before trying to extract tickers

    **Stock tickers to extract**

    :param ticker: single stock ticker/symbol/ETF to extract
    :param tickers: optional - list of tickers to extract
    :param use_key: optional - extract historical key from Redis
        usually formatted ``<TICKER>_<date formatted YYYY-MM-DD>``

    **(Optional) Data sources, datafeeds and datasets to gather**

    :param iex_datasets: list of strings for gathering specific `IEX
        datasets <https://iexcloud.io/>`__
        which are set as consts: ``analysis_engine.iex.consts.FETCH_*``.

    **(Optional) Redis connectivity arguments**

    :param redis_enabled: bool - toggle for auto-caching all
        datasets in Redis
        (default is ``True``)
    :param redis_address: Redis connection string format: ``host:port``
        (default is ``localhost:6379``)
    :param redis_db: Redis db to use
        (default is ``0``)
    :param redis_password: optional - Redis password
        (default is ``None``)
    :param redis_expire: optional - Redis expire value
        (default is ``None``)

    **(Optional) Minio (S3) connectivity arguments**

    :param s3_enabled: bool - toggle for auto-archiving on Minio (S3)
        (default is ``True``)
    :param s3_address: Minio S3 connection string format: ``host:port``
        (default is ``localhost:9000``)
    :param s3_bucket: S3 Bucket for storing the artifacts
        (default is ``dev``) which should be viewable on a browser:
        http://localhost:9000/minio/dev/
    :param s3_access_key: S3 Access key
        (default is ``trexaccesskey``)
    :param s3_secret_key: S3 Secret key
        (default is ``trex123321``)
    :param s3_region_name: S3 region name
        (default is ``us-east-1``)
    :param s3_secure: Transmit using tls encryption
        (default is ``False``)

    **(Optional) Celery worker broker connectivity arguments**

    :param celery_disabled: bool - toggle synchronous mode or publish
        to an engine connected to the `Celery broker and backend
        <https://github.com/celery/celery#transports-and-backends>`__
        (default is ``True`` - synchronous mode without an engine
        or need for a broker or backend for Celery)
    :param broker_url: Celery broker url
        (default is ``redis://0.0.0.0:6379/13``)
    :param result_backend: Celery backend url
        (default is ``redis://0.0.0.0:6379/14``)
    :param label: tracking log label

    **(Optional) Debugging**

    :param verbose: bool - show extract warnings
        and other debug logging (default is False)

    **Supported environment variables**

    ::

        export REDIS_ADDRESS="localhost:6379"
        export REDIS_DB="0"
        export S3_ADDRESS="localhost:9000"
        export S3_BUCKET="dev"
        export AWS_ACCESS_KEY_ID="trexaccesskey"
        export AWS_SECRET_ACCESS_KEY="trex123321"
        export AWS_DEFAULT_REGION="us-east-1"
        export S3_SECURE="0"
        export WORKER_BROKER_URL="redis://0.0.0.0:6379/13"
        export WORKER_BACKEND_URL="redis://0.0.0.0:6379/14"
    """

    rec = {}
    extract_requests = []

    use_tickers = tickers
    if ticker:
        use_tickers = [ticker]
    else:
        if not use_tickers:
            use_tickers = []

    default_iex_datasets = [
        'daily',
        'minute',
        'quote',
        'stats',
        'peers',
        'news',
        'financials',
        'earnings',
        'dividends',
        'company'
    ]

    if not iex_datasets:
        iex_datasets = default_iex_datasets

    if redis_enabled:
        if not redis_address:
            redis_address = os.getenv(
                'REDIS_ADDRESS',
                'localhost:6379')
        if not redis_password:
            redis_password = os.getenv(
                'REDIS_PASSWORD',
                None)
        if not redis_db:
            redis_db = int(os.getenv(
                'REDIS_DB',
                '0'))
        if not redis_expire:
            redis_expire = os.getenv(
                'REDIS_EXPIRE',
                None)
    if s3_enabled:
        if not s3_address:
            s3_address = os.getenv(
                'S3_ADDRESS',
                'localhost:9000')
        if not s3_access_key:
            s3_access_key = os.getenv(
                'AWS_ACCESS_KEY_ID',
                'trexaccesskey')
        if not s3_secret_key:
            s3_secret_key = os.getenv(
                'AWS_SECRET_ACCESS_KEY',
                'trex123321')
        if not s3_region_name:
            s3_region_name = os.getenv(
                'AWS_DEFAULT_REGION',
                'us-east-1')
        if not s3_secure:
            s3_secure = os.getenv(
                'S3_SECURE',
                '0') == '1'
        if not s3_bucket:
            s3_bucket = os.getenv(
                'S3_BUCKET',
                'dev')
    if not broker_url:
        broker_url = os.getenv(
            'WORKER_BROKER_URL',
            'redis://0.0.0.0:6379/13')
    if not result_backend:
        result_backend = os.getenv(
            'WORKER_BACKEND_URL',
            'redis://0.0.0.0:6379/14')

    if not label:
        label = 'get-latest'

    num_tickers = len(use_tickers)
    last_close_str = ae_utils.get_last_close_str()

    if iex_datasets:
        log.info(
            f'{label} - getting latest for tickers={num_tickers} '
            f'iex={json.dumps(iex_datasets)}')
    else:
        log.info(
            f'{label} - getting latest for tickers={num_tickers}')

    ticker_key = use_key
    if not ticker_key:
        ticker_key = f'{ticker}_{last_close_str}'

    common_vals = {}
    common_vals['base_key'] = ticker_key
    common_vals['celery_disabled'] = celery_disabled
    common_vals['ticker'] = ticker
    common_vals['label'] = label
    common_vals['iex_datasets'] = iex_datasets
    common_vals['s3_enabled'] = s3_enabled
    common_vals['s3_bucket'] = s3_bucket
    common_vals['s3_address'] = s3_address
    common_vals['s3_secure'] = s3_secure
    common_vals['s3_region_name'] = s3_region_name
    common_vals['s3_access_key'] = s3_access_key
    common_vals['s3_secret_key'] = s3_secret_key
    common_vals['s3_key'] = ticker_key
    common_vals['redis_enabled'] = redis_enabled
    common_vals['redis_address'] = redis_address
    common_vals['redis_password'] = redis_password
    common_vals['redis_db'] = redis_db
    common_vals['redis_key'] = ticker_key
    common_vals['redis_expire'] = redis_expire

    common_vals['redis_address'] = redis_address
    common_vals['s3_address'] = s3_address

    log.info(
        f'{label} - extract ticker={ticker} last_close={last_close_str} '
        f'base_key={common_vals["base_key"]} '
        f'redis_address={common_vals["redis_address"]} '
        f's3_address={common_vals["s3_address"]}')

    """
    Extract Datasets
    """

    iex_daily_status = ae_consts.FAILED
    iex_minute_status = ae_consts.FAILED
    iex_quote_status = ae_consts.FAILED
    iex_stats_status = ae_consts.FAILED
    iex_peers_status = ae_consts.FAILED
    iex_news_status = ae_consts.FAILED
    iex_financials_status = ae_consts.FAILED
    iex_earnings_status = ae_consts.FAILED
    iex_dividends_status = ae_consts.FAILED
    iex_company_status = ae_consts.FAILED
    yahoo_news_status = ae_consts.FAILED
    yahoo_options_status = ae_consts.FAILED
    yahoo_pricing_status = ae_consts.FAILED
    td_calls_status = ae_consts.FAILED
    td_puts_status = ae_consts.FAILED

    iex_daily_df = None
    iex_minute_df = None
    iex_quote_df = None
    iex_stats_df = None
    iex_peers_df = None
    iex_news_df = None
    iex_financials_df = None
    iex_earnings_df = None
    iex_dividends_df = None
    iex_company_df = None
    yahoo_option_calls_df = None
    yahoo_option_puts_df = None
    yahoo_pricing_df = None
    yahoo_news_df = None
    td_calls_df = None
    td_puts_df = None

    for ticker in use_tickers:
        req = api_requests.get_ds_dict(
            ticker=ticker,
            base_key=common_vals['base_key'],
            ds_id=label,
            service_dict=common_vals)
        extract_requests.append(req)
    # end of for all ticker in use_tickers

    extract_iex = True
    if extract_mode not in ['all', 'iex']:
        extract_iex = False

    extract_yahoo = True
    if extract_mode not in ['all', 'yahoo']:
        extract_yahoo = False

    extract_td = True
    if extract_mode not in ['all', 'td']:
        extract_td = False

    for extract_req in extract_requests:
        if 'daily' in iex_datasets or extract_iex:
            iex_daily_status, iex_daily_df = \
                iex_extract_utils.extract_daily_dataset(
                    extract_req)
            if iex_daily_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_daily={ticker}')
        if 'minute' in iex_datasets or extract_iex:
            iex_minute_status, iex_minute_df = \
                iex_extract_utils.extract_minute_dataset(
                    extract_req)
            if iex_minute_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_minute={ticker}')
        if 'quote' in iex_datasets or extract_iex:
            iex_quote_status, iex_quote_df = \
                iex_extract_utils.extract_quote_dataset(
                    extract_req)
            if iex_quote_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_quote={ticker}')
        if 'stats' in iex_datasets or extract_iex:
            iex_stats_df, iex_stats_df = \
                iex_extract_utils.extract_stats_dataset(
                    extract_req)
            if iex_stats_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_stats={ticker}')
        if 'peers' in iex_datasets or extract_iex:
            iex_peers_df, iex_peers_df = \
                iex_extract_utils.extract_peers_dataset(
                    extract_req)
            if iex_peers_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_peers={ticker}')
        if 'news' in iex_datasets or extract_iex:
            iex_news_status, iex_news_df = \
                iex_extract_utils.extract_news_dataset(
                    extract_req)
            if iex_news_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_news={ticker}')
        if 'financials' in iex_datasets or extract_iex:
            iex_financials_status, iex_financials_df = \
                iex_extract_utils.extract_financials_dataset(
                    extract_req)
            if iex_financials_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_financials={ticker}')
        if 'earnings' in iex_datasets or extract_iex:
            iex_earnings_status, iex_earnings_df = \
                iex_extract_utils.extract_earnings_dataset(
                    extract_req)
            if iex_earnings_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_earnings={ticker}')
        if 'dividends' in iex_datasets or extract_iex:
            iex_dividends_status, iex_dividends_df = \
                iex_extract_utils.extract_dividends_dataset(
                    extract_req)
            if iex_dividends_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_dividends={ticker}')
        if 'company' in iex_datasets or extract_iex:
            iex_company_status, iex_company_df = \
                iex_extract_utils.extract_company_dataset(
                    extract_req)
            if iex_company_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract iex_company={ticker}')
        # end of iex extracts

        if extract_yahoo:
            yahoo_options_status, yahoo_option_calls_df = \
                yahoo_extract_utils.extract_option_calls_dataset(
                    extract_req)
            yahoo_options_status, yahoo_option_puts_df = \
                yahoo_extract_utils.extract_option_puts_dataset(
                    extract_req)
            if yahoo_options_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract yahoo_options={ticker}')
            yahoo_pricing_status, yahoo_pricing_df = \
                yahoo_extract_utils.extract_pricing_dataset(
                    extract_req)
            if yahoo_pricing_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract yahoo_pricing={ticker}')
            yahoo_news_status, yahoo_news_df = \
                yahoo_extract_utils.extract_yahoo_news_dataset(
                    extract_req)
            if yahoo_news_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract yahoo_news={ticker}')
        # end of yahoo extracts

        if extract_td:
            td_calls_status, td_calls_df = \
                td_extract_utils.extract_option_calls_dataset(
                    extract_req)
            if td_calls_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract tdcalls={ticker}')
            td_puts_status, td_puts_df = \
                td_extract_utils.extract_option_puts_dataset(
                    extract_req)
            if td_puts_status != ae_consts.SUCCESS:
                if verbose:
                    log.warning(f'unable to extract tdputs={ticker}')
        # td extracts

        ticker_data = {}
        ticker_data['daily'] = iex_daily_df
        ticker_data['minute'] = iex_minute_df
        ticker_data['quote'] = iex_quote_df
        ticker_data['stats'] = iex_stats_df
        ticker_data['peers'] = iex_peers_df
        ticker_data['news1'] = iex_news_df
        ticker_data['financials'] = iex_financials_df
        ticker_data['earnings'] = iex_earnings_df
        ticker_data['dividends'] = iex_dividends_df
        ticker_data['company'] = iex_company_df
        ticker_data['calls'] = yahoo_option_calls_df
        ticker_data['puts'] = yahoo_option_puts_df
        ticker_data['pricing'] = yahoo_pricing_df
        ticker_data['news'] = yahoo_news_df
        ticker_data['tdcalls'] = td_calls_df
        ticker_data['tdputs'] = td_puts_df

        rec[ticker] = ticker_data
    # end of for service_dict in extract_requests

    return rec
# end of extract
