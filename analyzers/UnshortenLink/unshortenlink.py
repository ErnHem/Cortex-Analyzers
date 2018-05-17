#!/usr/bin/env python3
# encoding: utf-8

import requests
from cortexutils.analyzer import Analyzer

class UnshortenlinkAnalyzer(Analyzer):

    def __init__(self):
        Analyzer.__init__(self)
        self.url = self.getParam('url', None)
        self.proxies = self.getParam('config.proxy', None)

    def artifacts(self, raw):
        if raw['found'] == True:
            return [{'type': 'url', 'value': raw['url']}]
        else:
            return []

    def run(self):
        Analyzer.run(self)

        url = self.getData()

        if self.proxies:
            proxies = self.proxies
        else:
            proxies = {}

        try:
            response = requests.get(url, proxies=proxies, allow_redirects=False) 
    
            result = {'found': False, 'url': None}
        
            if (response.status_code == 301) or (response.status_code == 302):
                result['url'] = response.headers['Location']
                result['found'] = True
        except Exception as e:
            self.unexpectedError("Service unavailable: %s" % e)

        self.report(result)

if __name__ == '__main__':
    UnshortenlinkAnalyzer().run()
