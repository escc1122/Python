class Config:
    pwd:str = None
    can_change:str = "before"
    @classmethod
    def init_config(cls,pwd="123456",can_change=""):
        if cls.pwd is None:
            cls.pwd = pwd
            print("配置已初始化")
        else:
            print("配置已初始化，不可重复初始化")
        if can_change!="":
            cls.can_change = can_change


    @classmethod
    def getPwd(cls):
        return cls.pwd

    @classmethod
    def getCanChange(cls):
        return cls.can_change


