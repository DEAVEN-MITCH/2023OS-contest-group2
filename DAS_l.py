from BasePolicy import BasePolicy
from collections import defaultdict
import logging


class DAS_l(BasePolicy):
    def ProcessNewPage(self, pageNumber: int):        
        pages = self.pages
        self.lruSize = int(len(pages)*self.p)+1
        self.lfuSize = len(pages) - self.lruSize
        self.totalNumber += 1
        for page in pages:
            if page.valid:
                page.lastAccessed += 1
        for page in pages:
            if page.valid and page.addr == pageNumber:
                self.hitNumber += 1
                self.freq[page.addr] += 1
                page.lastAccessed = 0
                if self.lfuCount == self.lfuSize:
                    min_lfu_block = min([page for page in pages if page.lfu], key=lambda page: (self.freq[page.addr]))
                    if self.freq[min_lfu_block.addr] < self.freq[page.addr]:
                        page.lfu, min_lfu_block.lfu = True, False
                elif self.lfuCount < self.lfuSize:
                    page.lfu = True
                    self.lruCount -= 1
                    self.lfuCount += 1
                return
        if not self.allValid:
            for page in pages:
                if not page.valid:
                    page.valid = True
                    page.addr = pageNumber
                    self.freq[page.addr] += 1
                    page.lastAccessed = 0
                    if self.lruCount < self.lruSize:
                        self.lruCount += 1
                    else:
                        page.lfu = True
                        self.lfuCount += 1
                    return
        self.allValid = True
        lru_page = max([page for page in pages if not page.lfu], key=lambda page: page.lastAccessed)
        lru_page.addr = pageNumber
        self.freq[page.addr] += 1
        lru_page.lastAccessed = 0

    def SetUp(self):
        self.allValid = False
        self.lruCount = 0
        self.lfuCount = 0
        self.lfuSize = 0
        self.lruSize = 0
        self.p = 0.01    #LRU比例
        self.freq = defaultdict(int)

    def End(self):
        self.hitRate = self.hitNumber / self.totalNumber
