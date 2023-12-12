from BasePolicy import BasePolicy
import logging


class LRU(BasePolicy):
    def ProcessNewPage(self, pageNumber: int):
        pages = self.pages
        self.totalNumber += 1
        for page in pages:  # update recency first
            if page.valid:
                page.lastAccessed += 1
        for page in pages:
            if page.valid and page.addr == pageNumber:
                self.hitNumber += 1
                page.lastAccessed = 0
                return
        if not self.allValid:
            for page in pages:
                if not page.valid:
                    page.valid = True
                    page.addr = pageNumber
                    page.lastAccessed = 0
                    return
        self.allValid = True
        lru_page = max(pages, key=lambda page: page.lastAccessed)
        lru_page.addr = pageNumber
        lru_page.lastAccessed = 0

    def SetUp(self):
        self.allValid = False

    def End(self):
        self.hitRate = self.hitNumber / self.totalNumber
