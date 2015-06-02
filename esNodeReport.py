#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ElasticSearch Node report - Info

"""

__author__ = "Jash Lee"
__copyright__ = "May 29, 2015"
__credits__ = "Site Reliability Engineers"
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Jash Lee"
__email__ = "s905060@gmail.com"
__status__ = "Alpha"

import requests
import sys
#import argparse
""" Next time
# Argument checking
parser = argparse.ArgumentParser(description='ElasticSearch Node report')
parser.add_argument('-a', action="store", dest="arg", required=True)
argument = parser.parse_args()
"""
"""
Usage: esNodeReport.py {req_search_rejected | req_index_rejected | cache_evictions | fieldata_size | free_space}

"""

class ESNodeReport:
    def __init__(self, arg):
        self.arg = arg
        self.cluster = "http://localpriv:9200/_cluster/stats"
        self.nodes = "http://localpriv:9200/_nodes/_local/stats"
        self.clusterResponse = {}
        self.nodeResponse = {}

    def getClusterStatus(self):
        response = requests.get(self.cluster) # Send GET request
        self.clusterResponse = response.json()

    def getNodesStatus(self):
        response = requests.get(self.nodes) # Send GET request
        self.nodeResponse = response.json()

    def get_fs_total_free_in_bytes(self): # parsing JSON
        return self.clusterResponse['nodes']['fs']['free_in_bytes']  # Return Bytes

    def get_indices_filter_cache_evictions(self): # parsing JSON
        return self.clusterResponse['indices']['filter_cache']['evictions'] # Return Integer

    def get_indices_fielddata_memory_size_in_bytes(self): # parsing JSON
        return self.clusterResponse['indices']['fielddata']['memory_size_in_bytes'] # Return Bytes

    def get_thread_pool_index_rejected(self): # parsing JSON
        self.nodeResponse['nodes'].keys()
        key = self.nodeResponse['nodes'].keys()
        node = key[0]
        return self.nodeResponse['nodes'][node]['thread_pool']['index']['rejected'] # Return Integer

    def get_thread_pool_search_rejected(self): # parsing JSON
        self.nodeResponse['nodes'].keys()
        key = self.nodeResponse['nodes'].keys()
        node = key[0]
        return self.nodeResponse['nodes'][node]['thread_pool']['search']['rejected']

if __name__ == "__main__":

    # Story stats here
    argument = sys.argv[1]

    # Checking Argument
    if not argument in ["req_search_rejected", "req_index_rejected", "cache_evictions", "fieldata_size", "free_space"]:
        sys.exit()

    digger = ESNodeReport(argument) # Makes new instance
    digger.getClusterStatus() # Get info from cluster url
    digger.getNodesStatus() # Get info from nodes url

    if argument == "req_search_rejected": # Single Node Info
        thread_pool_search_rejected = digger.get_thread_pool_search_rejected()
        print thread_pool_search_rejected

    elif argument == "req_index_rejected": # Single Node Info
        thread_pool_index_rejected = digger.get_thread_pool_index_rejected()
        print thread_pool_index_rejected

    elif argument == "cache_evictions": # Cluster Info
        indices_filter_cache_evictions = digger.get_indices_filter_cache_evictions()
        print indices_filter_cache_evictions

    elif argument == "fieldata_size": # Cluster Info
        indices_fielddata_memory_size_in_bytes = digger.get_indices_fielddata_memory_size_in_bytes()
        print indices_fielddata_memory_size_in_bytes

    elif argument == "free_space": # Cluster Info
        get_fs_total_free_in_bytes = digger.get_fs_total_free_in_bytes()
        print get_fs_total_free_in_bytes

    else:
        sys.exit()
