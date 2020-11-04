#  Listens to nginx on /tmp/nginx.socket


def pre_fork(server, worker):
    with open('/tmp/app-initialized', 'w'):  # Creates file to tell nginx it's ready
        pass


bind = 'unix:/tmp/nginx.socket'
