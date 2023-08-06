import logging
import os
import re


logger = logging.getLogger(__name__)


r_docker = re.compile("\d+:[\w=]+:/docker(-[ce]e)?/\w+")


def is_docker_cgroup():
    pid = os.getpid()
    cgroup_path = os.path.join("/proc/", str(pid), "/cgroup")
    if not os.path.isfile(cgroup_path): 
        return False
    with open(path) as f:
        return any([r_docker.match(line) for line in f])


def is_inside_container():
    return is_docker_cgroup()
