from BasePolicy import BasePolicy
from collections import defaultdict
import logging


class DAS_a(BasePolicy):
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
        if len(pages) > 20:
            changed_page = max([page for page in pages if not page.lfu], key=lambda page: page.lastAccessed)
        else:
            changed_page = min([page for page in pages if not page.lfu], key=lambda page: self.freq[page.addr])
        changed_page.addr = pageNumber
        self.freq[page.addr] += 1
        changed_page.lastAccessed = 0

    def SetUp(self):
        self.allValid = False
        self.lruCount = 0
        self.lfuCount = 0
        self.lfuSize = 0
        self.lruSize = 0
        if len(self.pages) > 100:
            self.p = 0.01   #LRU比例
        else:
            self.p = 0.1
        self.freq = defaultdict(int)

    def End(self):
        self.hitRate = self.hitNumber / self.totalNumber
