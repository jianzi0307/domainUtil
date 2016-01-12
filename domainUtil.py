#!/usr/bin/python

import memcache, urllib2, optparse, xml.dom.minidom, time

''' memcache class '''
class Cache:
    def __init__(self, hostlist):
        self.__mc = memcache.Client(hostlist)

    def set(self, key, value):
        result = self.__mc.set(key, value)
        return result

    def get(self, key):
        result = self.__mc.get(key)
        return result

    def delete(self, key):
        result = self.__mc.delete(key)
        return result

''' domain tools class '''
class DomainUtil:
    ''' parse xml '''
    def parseXml(self, x):
        x = x.decode('gbk').encode('utf-8') 
        x = x.replace('gb2312', 'utf-8')
        dom = xml.dom.minidom.parseString(x)
        root = dom.documentElement
        return root

    ''' get xml node value '''
    def nodeValue(self, xmlStr):
        root = self.parseXml(xmlStr)
        node = root.getElementsByTagName('original')
        s = node[0].firstChild.data
        status, msg = s.split(':')
        return status, msg 

    ''' batch get domain register info '''
    def main(self):
        url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain='
        cache = Cache(['127.0.0.1:20000'])
        char = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
        output = open('domain.txt', 'a')
        for i in range(len(char)):  
            a = char[i]
            for j in range(len(char)):
                b = char[j]
                for i in range(0, 9):
                    domain = a + b + str(i) + '.com'
                    if cache.get(domain) == 1:
                        print domain + ' has cached.'
                        continue
                    dUrl = url + domain
                    xmlStr = urllib2.urlopen(dUrl).read(1000)
                    status, msg = self.nodeValue(xmlStr)
                    output.write(domain + "\t" + msg.strip() + "\n")
                    cache.set(domain, 1)
                    time.sleep(1)
                    print "--->" + domain
        output.close()

if __name__ == '__main__':
    #url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain='
    dUtil = DomainUtil()
    dUtil.main()

