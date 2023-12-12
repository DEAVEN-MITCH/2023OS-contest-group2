from abc import ABCMeta, abstractmethod


class BasePolicy(metaclass=ABCMeta):
    @abstractmethod
    def ProcessNewPage(self, pageNumber: int):
        """This method must be implemented to process each page number"""
        pass

    def GetOutput(self) -> str:
        """This method can be overridden to return the Statistical output in the format of str"""
        return f"{type(self).__name__}\t{len(self.pages)}\t{self.totalNumber}\t{self.hitNumber}\t{self.hitRate}\n"

    def GetHeader() -> str:
        """This method can be overridden to return the header of the statistical output in the format of str"""
        return f"policy\tframeNumber\ttotalNumber\thitNumber\thitRate\n"

    def __init__(self, parameter: list, commonPolicyParameters: dict, pages: tuple):
        """You had better not override this method unless you are experienced in dealing with Python's 继承
        parameter is the specified policy's parameter configured in the json file in a list form
        commonPolicyParameters also derives from the json file
        pages by default will be created as new by PageManager and passed here in a tuple form you may use len(pages) to get its size.Replace it with your customized pages in SetUp function if necessary
        """
        self.parameter = parameter
        self.commonPolicyParameters = commonPolicyParameters
        self.pages = pages
        self.totalNumber = 0
        self.hitNumber = 0
        self.hitRate = 0

    def SetUp(self):
        """You can override this method to initialize your customized pages or do something with your parameters"""
        pass

    def End(self):
        """You can override this method to calculate the final statistics for output"""
        pass
