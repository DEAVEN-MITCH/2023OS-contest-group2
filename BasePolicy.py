from abc import ABCMeta, abstractmethod


class BasePolicy(metaclass=ABCMeta):
    @abstractmethod
    def ProcessNewPage(self,pageNumber:int):
        '''This method must be implemented to process each page number'''
        pass
    @abstractmethod
    def GetOutput(self)->str:
        '''This method must be implemented to return the Statistical output in the format of str'''
        pass
    def __init__(self,parameter:list,commonPolicyParameters:dict,pages:tuple):
        '''You had better not override this method unless you are experienced in dealing with Python's 继承
        parameter is the specified policy's parameter configured in the json file in a list form
        commonPolicyParameters also derives from the json file
        pages by default will be created as new by PageManager and passed here in a tuple form you may use len(pages) to get its size.Replace it with your customized pages in SetUp function if necessary
        '''
        self.parameter=parameter
        self.commonPolicyParameters = commonPolicyParameters
        self.pages=pages
        self.totalNumber=0
        self.hitNumber=0
    def SetUp(self):
        '''You can override this method to initialize your customized pages or do something with your parameters'''
        pass
    def End(self):
        '''You can override this method to calculate the final statistics for output'''
        pass

