'''
Created on Dec 7, 2012

@author: hoekstra
'''
import argparse
import re

class Converter(object):
    '''
    classdocs
    '''


    def __init__(self, redactiebladen):
        '''
        Constructor
        '''
        self.rb = redactiebladen
        self.rb_pos = 0
        self.last = []
        self.prev_line = ""
        
    def __iter__(self):
        return self
        
    def next(self):
        pub_lines = []
        
        started = False
        count = self.rb_pos
        
        if count != 0 :
            pub_lines.append(self.prev_line)
        
        for line in self.rb:
#            print count
            count = count + 1
            if line.startswith('SET') and not started :
                started = True
            elif line.startswith('SET') and started :
                self.prev_line = line.strip('\n')
                started = False
                break
            elif line == '\n' :
                continue
            elif line.endswith('-\n') :
                self.prev_line = line.strip("\n")
                continue
            
            pub_lines.append(self.prev_line + line.strip("\n"))
            self.prev_line = ""
        
        print pub_lines
        self.rb_pos = count
        
        if len(pub_lines) > 1:
            self.current = pub_lines
            return pub_lines
        else :
            raise StopIteration
        
    def parse(self):

        first = r'SET\:\s(?P<set>\w+\s.+?)\sTTL\:\s(?P<ttl>\d+)\sPPN\:\s(?P<ppn>\d{9})\sPAG\:\s(?P<pag>\d+)\s\.'
        mfirst = re.search(first,self.current[0])
        
        second = r'Ingevoerd\:\s(?P<ingevoerd>\d{4}\:\d\d-\d\d-\d\d)\sGewijzigd\:\s(?P<gewijzigd>\d{4}\:\d\d-\d\d-\d\d\s\d\d\:\d\d:\d\d)\sStatus:\s(?P<status>\d{4}\:\d\d-\d\d-\d\d)'
        msecond = re.search(second,self.current[1])
        
        ppn = mfirst.group('ppn')
        ingevoerd = msecond.group('ingevoerd')
        
        print ppn, ingevoerd
        
        for l in self.current[2:]:
            print l
        
        
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # ../../STCN/data/redactiebladen/alleredacs.checked.1.txt
    parser.add_argument("redactiebladen",nargs="?", type=str, help="Filename of the STCN redactiebladen dump",default='test.txt')
    
    args = parser.parse_args()
    
    redactiebladen = open(args.redactiebladen,"r")
    
    c = Converter(redactiebladen)
    
    c.next()
    c.parse()
