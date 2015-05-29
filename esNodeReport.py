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
        self.cluster = "http://localhost:9200/_cluster/stats"
        self.nodes = "http://localhost:9200/_nodes/_local/stats"

    def getClusterStatus(self):
        response = requests.get(self.cluster) # Send GET request
        decodedJson = response.json()
        return decodedJson

    def getNodesStatus(self):
        response = requests.get(self.nodes) # Send GET request
        decodedJson = response.json()
        return decodedJson

    def get_fs_total_free_in_bytes(self, inputs): # parsing JSON
        return inputs['fs']['total']['free_in_bytes']  # Return Bytes

    def get_indices_filter_cache_evictions(self, inputs): # parsing JSON
        return inputs['indices']['filter_cache']['evictions'] # Return Integer

    def get_indices_fielddata_memory_size_in_bytes(self, inputs): # parsing JSON
        return inputs['indices']['fielddata']['memory_size_in_bytes'] # Return Bytes

    def get_thread_pool_index_rejected(self, inputs): # parsing JSON
        return inputs['nodes']['thread_pool']['index']['rejected'] # Return Integer

    def get_thread_pool_search_rejected(self, inputs): # parsing JSON
        return inputs['nodes']['thread_pool']['search']['rejected']

if __name__ == "__main__":

    # Story stats here
    argument = sys.argv[1]

    # Checking Argument
    if not argument in ["req_search_rejected", "req_index_rejected", "cache_evictions", "fieldata_size", "free_space"]:
        sys.exit()

    digger = ESNodeReport(argument) # Makes new instance
    clusterDecodedJson = digger.getClusterStatus() # Get info from cluster url
    nodesDecodedJson = digger.getNodesStatus() # Get info from nodes url

    if argument == "req_search_rejected": # Single Node Info
        thread_pool_search_rejected = digger.get_thread_pool_search_rejected(nodesDecodedJson)
        print thread_pool_search_rejected

    elif argument == "req_index_rejected": # Single Node Info
        thread_pool_index_rejected = digger.get_thread_pool_index_rejected(nodesDecodedJson)
        print thread_pool_index_rejected

    elif argument == "cache_evictions": # Cluster Info
        indices_filter_cache_evictions = digger.get_indices_filter_cache_evictions(clusterDecodedJson)
        print indices_filter_cache_evictions

    elif argument == "fieldata_size": # Cluster Info
        indices_fielddata_memory_size_in_bytes = digger.get_indices_fielddata_memory_size_in_bytes(clusterDecodedJson)
        print indices_fielddata_memory_size_in_bytes

    elif argument == "free_space": # Cluster Info
        get_fs_total_free_in_bytes = digger.get_indices_filter_cache_evictions(clusterDecodedJson)
        print get_fs_total_free_in_bytes

    else:
        sys.exit()
