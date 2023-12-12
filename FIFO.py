from BasePolicy import BasePolicy
import logging
class FIFO(BasePolicy):
    def ProcessNewPage(self,pageNumber:int):
        pages=self.pages
        self.totalNumber+=1
        for page in pages:
            if page.valid and page.addr ==pageNumber:
                self.hitNumber+=1
                return
        if not self.allValid:   
            for page in pages:
                if not page.valid:
                    page.valid = True
                    page.addr = pageNumber
                    return
        self.allValid = True
        pages[self.cursor].addr = pageNumber
        self.cursor=(self.cursor+1)%len(pages)

    def GetOutput(self)->str:
        return f'policy\ttotalNumber\thitNumber\thitRate\nFIFO\t{self.totalNumber}\t{self.hitNumber}\t{self.hitRate}\n'
    def SetUp(self):
        self.allValid = False
        self.cursor=0
        
    def End(self):
        self.hitRate=self.hitNumber/self.totalNumber
        # logging.debug('FIFO end')