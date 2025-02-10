from time import sleep
import requests
import numpy as np
import os

def retried_request(url, method="GET", data=None, params=None, headers=None, retries=8, timeout=10):
    """
    Retried request function with exponential backoff

    Parameters
    ----------
    url : str
        URL to request
    method : str, optional
        HTTP method, by default "GET"
    data : str, optional
        Request data, by default None
    headers : dict, optional
        Request headers, by default None
    retries : int, optional
        Number of retries, by default 8
    timeout : int, optional
        Request timeout, by default 10

    Returns
    -------
    requests.Response
        Response object

    Raises
    ------
    requests.RequestException
        If request fails

    """
    retried = 0
    while retried < retries:
        try:
            resp = requests.request(
                method=method, url=url, data=data, params=params, headers=headers, timeout=timeout
            )
            # Bad Gateway results in waiting for 10 seconds
            # and retrying
            if resp.status_code == 502:
                # time.sleep(10)
                raise requests.RequestException
        except (
            requests.RequestException,
            requests.ReadTimeout,
            requests.ConnectionError,
            requests.ConnectTimeout,
        ) as e:
            sleep(0.1 * 2**retried)
            retried += 1
            with open("/tmp/retried.log", "a") as f:
                f.write(f"{str(np.datetime64('now'))} Retrying request {url} {retried}/{retries} following error: {e}\n")
        else:
            return resp
