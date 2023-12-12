from BasePolicy import BasePolicy
import logging


class Second_chance(BasePolicy):
    def ProcessNewPage(self, pageNumber: int):
        pages = self.pages
        self.totalNumber += 1
        for page in pages:
            if page.valid and page.addr == pageNumber:
                self.hitNumber += 1
                page.accessCount = 1
                return
        if not self.allValid:
            for page in pages:
                if not page.valid:
                    page.valid = True
                    page.addr = pageNumber
                    page.accessCount = 1
                    return
        self.allValid = True
        while True:
            if pages[self.cursor].accessCount == 0:
                pages[self.cursor].addr = pageNumber
                self.cursor = (self.cursor + 1) % len(pages)
                return
            else:
                pages[self.cursor].accessCount = 0
                self.cursor = (self.cursor + 1) % len(pages)

    def SetUp(self):
        self.allValid = False
        self.cursor = 0

    def End(self):
        self.hitRate = self.hitNumber / self.totalNumber
