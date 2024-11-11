from .ali import AliService
from .singleton import Singleton
from .tencent import TencentService
from .service_interface import CloudServiceInterface
from enum import Enum


class ServiceProvider(Enum):
    ALI = "ali"
    TENCENT = "tencent"
    SINGLETON = "singleton"

class CloudServiceFactory:
    @staticmethod
    def create_service(service_provider: ServiceProvider) -> CloudServiceInterface:
        """
        根据传入的服务提供者（service_provider），创建并返回相应的云服务实例。

        此工厂方法负责生成不同类型的云服务实例，以便调用方通过统一的接口（CloudServiceInterface）
        来与具体的云服务进行交互。具体的实例类型取决于传入的服务提供者的具体类型。
        Args:
            service_provider: ServiceProvider 实例，用于指示需要创建的云服务类型

        Returns:
            CloudServiceInterface 实例，表示指定的云服务接口实现类

        Raises:
            ValueError: 如果 service_provider 类型不受支持，可能抛出此异常

        """
        if service_provider == ServiceProvider.ALI:
            return AliService("Ali Cloud Service")
        elif service_provider == ServiceProvider.TENCENT:
            return TencentService("Tencent Cloud Service")
        elif service_provider == ServiceProvider.SINGLETON:
            Singleton("Singleton Cloud Service")
            return Singleton("test Singleton")
        else:
            raise ValueError(f"Unknown service provider: {service_provider}")
