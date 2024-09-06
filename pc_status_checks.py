#!/usr/bin/env python3


## Script to check computer health
# Source: https://github.com/google/it-cert-automation/blob/master/Course3/repos/health-checks/health_checks.py


# OS routines for NT or Posix depending on what system we're on
import os

# Utility functions for copying and archiving files and directory trees
import shutil

# psutil is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python.
import psutil

# Provides socket operations and some related functions
import socket


def check_reboot():
    """Returns True if the computer has a pending reboot."""
    # File that's created on our computer when some software requires a reboot
    return os.path.exists("/run/reboot-required")


def check_disk_full(disk, min_gb, min_free_percent):
    """Returns True if there isn't enough disk space, False otherwise."""
    du = shutil.disk_usage(disk)
    # Calculate the percentage of free space
    percent_free = 100 * du.free / du.total
    # Calculate how many free gigabytes
    gigabytes_free = du.free / 2**30
    if percent_free < min_free_percent or gigabytes_free < min_gb:
        return True
    return False


def check_root_full():
    """Returns True if the root partition is full, False otherwise."""
    return check_disk_full(disk="/", min_gb=2, min_free_percent=10)


def check_cpu_constrained():
    """Returns True if the CPU is having too much usage (over 75%), False otherwise."""
    return psutil.cpu_percent(1) > 75


def check_no_network():
    """Returns True if it fails to resolve Google's URL, False otherwise."""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True


def main():
    checks = [
        (check_reboot, "Pending Reboot."),
        (check_root_full, "Root partition full"),
        (check_cpu_constrained, "CPU load too high"),
        (check_no_network, "No working network."),
    ]
    everything_ok = True

    # To allow printing more than one error message
    for check, msg in checks:
        if check():
            print(msg)
            everything_ok = False

    if everything_ok:
        print("Everything OK")


main()
