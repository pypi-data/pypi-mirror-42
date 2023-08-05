from macrobase_driver.config import DriverConfig


class AiopikaDriverConfig(DriverConfig):

    LOGO: str = """
 _____       _
|  __ \     (_)               
| |  | |_ __ ___   _____ _ __ 
| |  | | '__| \ \ / / _ \ '__|
| |__| | |  | |\ V /  __/ |   
|_____/|_|  |_| \_/ \___|_|aiopika
"""

    RABBITMQ_QUEUE: str = 'rpc_queue'

    RABBITMQ_USER: str = 'rabbitmq'
    RABBITMQ_PASS: str = 'test'
    RABBITMQ_HOST: str = 'localhost'
    RABBITMQ_PORT: int = 5672
    RABBITMQ_VHOST: str = '/'
