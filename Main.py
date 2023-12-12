import json
import logging  
import importlib  
class Page:
    def __init__(self):
        self.valid = False
        self.dirty = False
        self.lastAccessed = 0
        self.accessCount = 0
        self.addr =0
class PageManager:
    def __init__(self,config:dict):
        self.frameNumber = config['frameNumber']
        self.testPolicies = config['testPolicies']
        self.policyParameters = config['policyParameters']
        self.commonPolicyParameters=config['commonPolicyParameters']
        self.outputFile = open(config['outputFile'],'wt')
        self.traceFile = config['traceFile']
        # self.pages=(page() for i in range(frameNumber))
    def MakeNewpages(self):
        self.pages=tuple([Page() for i in range(self.frameNumber)])#tuple
    def Run(self):
        for policyName in self.testPolicies:
            self.currentPolicy = policyName
            parameter = self.policyParameters[policyName]
            for traceFile in self.traceFile:
                logging.debug(f"new start policy:{policyName};traceFile:{traceFile};parameter:{parameter}")
                self.MakeNewpages()
                # logging.debug(policyName)
                policyModule =  importlib.import_module(policyName)
                policyClass = getattr(policyModule,policyName)
                policy=policyClass(*self.MakePolicyParameter(parameter))#为每个traceFile实例化一个policy对象
                self.ProcessEachPolicy(policy,traceFile)
                logging.debug(f'end policy:{policyName};traceFile:{traceFile};parameter:{parameter}')
        self.End()
    def ProcessEachPolicy(self,policy,traceFile):
        policy.SetUp()
        with open(traceFile,'r') as f:
            for line in f: 
                pageNumber = int(line,16)#convert hex string to int
                policy.ProcessNewPage(pageNumber)
        policy.End()
        output = policy.GetOutput()
        self.outputFile.write(output)

    def MakePolicyParameter(self,parameter):
        return parameter,self.commonPolicyParameters,self.pages
    def End(self):
        self.outputFile.close()
# 设置日志级别为DEBUG，并将日志信息输出到'debug.log'文件中  
logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='w')  
  
# 输出Debug信息  
# logging.debug('这是一条Debug信息')
if __name__ == '__main__':
    
    config = {}
    with open('conf.json', 'r') as f:  
        config = json.load(f)#now config is a dict
    logging.debug(config)
    pageManager = PageManager(config)
    pageManager.Run()
    pass