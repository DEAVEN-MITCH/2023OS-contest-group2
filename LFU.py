from BasePolicy import BasePolicy
import logging


class LFU(BasePolicy):
    def ProcessNewPage(self, pageNumber: int):
        pages = self.pages
        self.totalNumber += 1
        for page in pages:
            if page.valid and page.addr == pageNumber:
                self.hitNumber += 1
                page.accessCount += 1
                return
        if not self.allValid:
            for page in pages:
                if not page.valid:
                    page.valid = True
                    page.addr = pageNumber
                    page.accessCount = 1
                    return
        self.allValid = True
        lfu_page = min(pages, key=lambda page: page.accessCount)
        lfu_page.addr = pageNumber
        lfu_page.accessCount = 1

    def SetUp(self):
        self.allValid = False

    def End(self):
        self.hitRate = self.hitNumber / self.totalNumber
