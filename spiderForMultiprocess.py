#coding=UTF-8
'''
Created on 2012-2-29

@author: 凌
'''
import os,re,urllib2,string,logging
from urlparse import urlparse
import multiprocessing
import BeautifulSoup
#import G_value
def getLinks(filepath):
        #self.filepath=self.path(self.url)
        op=open(filepath).read()
        link=op.split(' ')
        return link
def downloader(url,filepath):
    
    try:
        f=urllib2.urlopen(url).read()
    except:
        return 'Dead Link：%s' %url
    op=open(filepath,'wb')
    ext=os.path.splitext(filepath)
    if ext[1]=='.css' or ext[1]=='.js':
        try:
            op.write(f)
        finally:
            op.close()
    else:
        
        soup=BeautifulSoup.BeautifulSoup(f)
        try:
            value=[]
            for a in soup.findAll('a'):
                value.append(a['href'])
            op.write(' '.join(value))
        except:
            print 'Faild to write data into %s' %filepath
        finally:
            op.close()
def spider(parameter):
    #if G_value.count>G_value.countmax:
    #    return
    if len(parameter)!=3:
        return 'spider parameter error'
    url,count,seen=parameter
    pretr=pretreat(url)
    url,dom=pretr
    path=filepath(url)
    q=[]
    try:
        downloader(url,path)
    except:
        return 'continue'   
    print "\n("+str(count)+")"+"URL:"+url
    #seen.append(url)
    #G_value.count=G_value.count+1
    links=getLinks(path)
    for eachLink in links:
        if eachLink[:4]!="http"and string.find(eachLink,"://")==-1:
            #print "*",eachLink
            continue
        if string.find(string.lower(eachLink),"mailto:")!=-1:
            #print "...discard,mail to link"
            continue
        if string.find(string.lower(eachLink),"javascript")!=-1:
            #print '...false url'
            continue
        if eachLink not in seen:
            if string.find(eachLink,dom)==-1:
                #print "...discarded,not in domain"
                continue
            else:
                if eachLink not in q:
                    q.append(eachLink)
                    #print "...new,added to Q :",eachLink 
                else:
                    #print "...discarded,already in Q"
                    continue
        else:
            #print "...discarded,already processed"
            continue
    return q
def go(url,countmax=65535):
    q=[url]
    seen=[]
    p=[]
    count=0
    pool_size=multiprocessing.cpu_count()
    while q and count<countmax:
        while count<countmax and q:
            count+=1
            u=q.pop()
            seen.append(u)
            p.append([u,count,seen])
            logging.info('Spider downloading url:%s'%u)
        pool=multiprocessing.Pool(processes=pool_size,initializer=start_pro)
        result=pool.map(spider,p)
        pool.close()
        pool.join()
        while p:
            p.pop()
        while result:
            newlist=result.pop()
            for newurl in newlist:
                if newurl not in seen:
                    if newurl not in q:
                        q.append(newurl)
                        print 'New url added to Q:%s' %newurl
def pretreat(url):
    qr=re.match(r'http(s?)://',url)
    if not qr:
        url='http://'+url
    dom='.'.join(urlparse(url).hostname.split('.')[1:])
    value=[url,dom]
    return value
def filepath(url):
    parsed = urlparse(url)
    path=parsed.hostname+parsed.path
    if not parsed.path:
        path+='/index.html'
    if path[-1]=='/':
        path+='index.html'
    if not os.path.splitext(path)[1]:
        path+='.html'
    filedir=os.path.dirname(path)
    if os.path.exists(filedir):
        if os.path.isdir(filedir):
            print '\ndir %s exists' %filedir
            return path
        else:
            os.remove(filedir)
            print '\nremove file'
    try:
        os.makedirs(filedir)
        print "\nmaking dir: %s" %filedir
    except OSError,why:
        print "\nFaild:%s" %str(why)
    return path        
def start_pro():
    print 'starting a new process.'
#def loggerfuc(lvl):
    
#    return logger
    
    
def main(site=None,max_size=None,log_level=logging.DEBUG):
    LEVELS={'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'critical':logging.CRITICAL}
    loglevel=LEVELS.get(log_level,logging.DEBUG)
    #log=multiprocessing.log_to_stderr(loglevel)
    logger=logging.getLogger()
    filehandler=logging.FileHandler('spider.log','a')
    streamhandler=logging.StreamHandler()
    fmt=logging.Formatter('[%(asctime)s] %(levelname)s:%(message)s')
    filehandler.setFormatter(fmt)
    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)
    logger.setLevel(loglevel)
    logging.info('LOGGING FOR SPIDER STARTS')
    #log.addHandler(filehandler)
    #logger=loggerfuc(log_level)'''
    
    try:
        if max_size==None :
            countmax=int(raw_input("Enter max No. of web:"))
        else:
            countmax=int(max_size)
        if site==None:
            url=raw_input("Enter starting URL:")
        else:
            url=site
    except(KeyboardInterrupt,EOFError):
        return "...Invalid Input"       
    #if os.path.exists('spider.log'):
        #os.remove('spider.log')
    go(url,countmax)
    logging.shutdown()
if __name__ == "__main__":
    
    main()
    print 'spider end.'