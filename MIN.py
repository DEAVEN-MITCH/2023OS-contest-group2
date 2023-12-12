from BasePolicy import BasePolicy
import logging


class MIN(BasePolicy):
    def ProcessNewPage(self, pageNumber: int):
        index = self.totalNumber
        tracelist = self.tracelist  # [pageNumber,nindex]
        tracedict = self.tracedict  # pageNumber:index
        if pageNumber in tracedict:
            pindex = tracedict[pageNumber]
            tracelist[pindex][1] = index  # 下一个相同pageNumber的index
        tracelist.append([pageNumber, None])  # 加入新的[pageNumber,nindex]
        tracedict[pageNumber] = index
        self.totalNumber += 1  # 下标

    def SetUp(self):
        self.allValid = False
        self.tracelist = []
        self.tracedict = {}

    def End(self):
        pages = self.pages
        tracelist = self.tracelist
        self.totalNumber = size = len(tracelist)
        for index, [pageNumber, nindex] in enumerate(tracelist):
            fin = False
            for page in pages:
                if page.valid and page.addr == pageNumber:
                    self.hitNumber += 1
                    page.nindex = nindex
                    fin = True
                    break
            if fin:
                continue
            if not self.allValid:
                for page in pages:
                    if not page.valid:
                        page.valid = True
                        page.addr = pageNumber
                        page.nindex = nindex
                        fin = True
                        break
            if fin:
                continue
            self.allValid = True
            min_page = max(
                pages, key=lambda page: page.nindex if page.nindex is not None else size
            )
            min_page.addr = pageNumber
            min_page.nindex = nindex

        self.hitRate = self.hitNumber / self.totalNumber
