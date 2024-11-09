from simple_code2 import TEST_CONST
from simple_code2.cloud import CloudServiceFactory, ServiceProvider
from simple_code2.cloud.tencent import TencentService

if __name__ == '__main__':
    # 根據需要選擇服務提供者
    service_provider = ServiceProvider.TENCENT  # 或者 CloudServiceFactory.ServiceProvider.ALI

    # 使用工廠創建服務
    cloud_service = CloudServiceFactory.create_service(service_provider)

    print(TencentService("直接呼叫").show())

    # 使用服務
    print(
        cloud_service.show())

    print(TEST_CONST)
