from BasePolicy import BasePolicy
import logging
import random


class Random(BasePolicy):
    def ProcessNewPage(self, pageNumber: int):
        pages = self.pages
        self.totalNumber += 1
        for page in pages:
            if page.valid and page.addr == pageNumber:
                self.hitNumber += 1
                return
        if not self.allValid:
            for page in pages:
                if not page.valid:
                    page.valid = True
                    page.addr = pageNumber
                    return
        self.allValid = True
        randomIndex = random.randint(0, len(pages) - 1)
        pages[randomIndex].addr = pageNumber

    def SetUp(self):
        self.allValid = False

    def End(self):
        self.hitRate = self.hitNumber / self.totalNumber
