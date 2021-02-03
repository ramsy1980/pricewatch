import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = 'gunicorn.log'
errorlog = 'gunicorn.error.log'
capture_output = True