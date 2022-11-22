from threading import Thread
import base64
import os
import time




class WorkDaemon(Thread):
    '''
    A daemon thread
    '''
    def __init__(self,work_method, interval,run_once=False,params=None,run_first_time=True):
        '''
        @param work_method: the referenced method/function.
        @param interval: interval in seconds
        @run_once: True if the process is ment to run only once  
        '''
        Thread.__init__(self)
        self.work_method=work_method
        self.daemon=True
        self.interval=interval
        self.paused=False
        self.run_once=run_once
        self.once_counter=0
        self.params=params
        self.idt=base64.urlsafe_b64encode(os.urandom(4))
        #print 'Thread created Run once ', self.run_once
        self.stopped=False
        self.run_first_time=run_first_time
    
    def run(self):
        
        while(True):
            if(self.stopped):
                return
            if(not self.paused):
                if(self.once_counter==0 and self.run_first_time==False):
                    self.once_counter+=1        
                    time.sleep(self.interval)
                    continue
                
                if(not self.run_once):
                    #print 'Excuting ',self.idt
                    if(self.params==None):
                        self.work_method()
                    else:
                        self.work_method(self.params)
                        
                elif(self.once_counter==1):
                    #print 'Executing once ',self.idt
                    if(self.params==None):
                        self.work_method()
                    else:
                        self.work_method(self.params)
                    return #execute just 1 one time after first interval comes up  
            #print('Incrementing once counter')    
            self.once_counter+=1        
            time.sleep(self.interval)
    def pause(self):
        self.paused=True
        
    def unpause(self):
        self.paused=False
        
    def stop(self):
        self.stopped=True
