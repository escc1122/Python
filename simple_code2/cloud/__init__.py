from .service_factory import CloudServiceFactory,ServiceProvider
from .config import Config


print(f"before {Config.getCanChange()}")
Config.init_config("password","after")
print(f"after {Config.getCanChange()}")




# 定義 __all__，只公開工廠方法
__all__ = ["CloudServiceFactory","ServiceProvider"]
