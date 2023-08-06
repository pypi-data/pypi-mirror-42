#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***
"""
import threading

from concurrent.futures import ThreadPoolExecutor, as_completed


import gc
import time
import requests
from memory_profiler import profile
# from concurrent.futures import ThreadPoolExecutor, as_completed

class getsession(object):
    def __init__(self):
        pass

    #@staticmethod
    def getnew(self):
        sess = requests.session()
        return sess

class runnerx(threading.Thread):

    def __init__(self, sess):
        threading.Thread.__init__(self)
        self.sess = sess.getnew()

    @profile
    def work(self):
        for i in range(10):
            response = self.sess.get('http://127.0.0.1:4567')
            a = response.content

        pass

    @profile
    def run(self):
        self.work()

@profile
def run_thread_request(sess, run):

#    with sess.__class__.getnew() as s:
    with sess.getnew() as s:
    #    with requests.session() as s:
        #s.headers.update({'Connection': 'close'})
        response = s.get('http://127.0.0.1:4567')
        #response.close()
        #doomy = response.content
        # del s
    return

@profile
def main():
#    sess = requests.session()
    # sessions = getsession()
    sessions = None

    with ThreadPoolExecutor(max_workers=1) as executor:
        print('Starting!')
        tasks = {executor.submit(run_thread_request, sessions, run):
                    run for run in range(1)}
        for _ in as_completed(tasks):
            pass
    print('Done!')
    return

@profile
def calling():
    # main()
    # for i in range(20):
    #     with requests.session() as s:
    #         #s.headers.update({'Connection': 'close'})
    #         response = s.get('https://www.google.com')
    #         response.close()
    #         doomy = response.content
    #         del response
    #         #del s

    sessinos = getsession()
    for i in range(5):
        new_client = runnerx(sessinos)

        new_client.start()
        new_client.join()  # commenting this out -> multi-threaded processing

    gc.collect()
    print("done xxxx")
    time.sleep(10000)

    return


if __name__ == '__main__':
    calling()