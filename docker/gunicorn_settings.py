import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
error_log_format = '{"request": "%(r)s", "http_status_code": "%(s)s", "http_request_url": "%(U)s", "http_query_string": "%(q)s", "http_verb": "%(m)s", "http_version": "%(H)s"}'