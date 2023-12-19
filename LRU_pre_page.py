from BasePolicy import BasePolicy
import logging

class LRU_pre_page(BasePolicy):
    
    def SetUp(self):
        self.capacity = self.commonPolicyParameters['capacity']
        self.cache = {}
        self.order = []  # 用于维护访问顺序的列表
        self.allValid = False
        self.imworkset = False
        
    def ProcessNewPage(self, pageNumber: int):
        self.access_page(pageNumber)
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
        self.UseWorkingSetToUpdatePages(pageNumber)
        #处理完主访问页后开始预取所有工作集里面的元素
            
            
            
            
        
    def End(self):
        self.hitRate = self.hitNumber / self.totalNumber
        
    def access_page(self, pageNumber:int):
        # 如果页面已在工作集中，更新其访问时间
        if pageNumber in self.cache:
            self.order.remove(pageNumber)
            self.order.append(pageNumber)
        else:
            # 如果工作集已满，移除最久未使用的页面
            if len(self.order) >= self.capacity:
                oldest_page = self.order.pop(0)
                del self.cache[oldest_page]

            # 将新页面添加到工作集
            self.cache[pageNumber] = True
            self.order.append(pageNumber)

    def get_working_set(self):
        return self.order
    
    def UseWorkingSetToUpdatePages(self,mainAccessNumber:int):
        # 取得工作集
        working_set = self.get_working_set()
        #对工作集里的每一个元素都按照对主访问页里面的逻辑处理一次
        # 不同之处在于不需要修改totalNumber和hitNumber
        for pageNumber in working_set:
            pages = self.pages
            # self.totalNumber += 1
            for page in pages:  # update recency first
                if page.valid:
                    pass
                    page.lastAccessed += 1
            for page in pages:
                if page.valid and page.addr == pageNumber:
                    # self.hitNumber += 1
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
        
            
        
# 示例
# k = 3  # 工作集大小
# trace = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]  # 输入的 trace 序列

# lrucache = LRU_pre_page(k)

# for page in trace:
#     lrucache.access_page(page)
#     working_set = lrucache.get_working_set()
#     print(f"Working Set: {working_set}")

#处理逻辑，每次读取新的页的时候get_working_set得到工作集，然后把整个工作集一起读进内存（不在内存里的部分），读的时候如果发现内存已满则调用大家设计的内存替换算法（任意一种即可），这里涉及到计数和最后计算结果