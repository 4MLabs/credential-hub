class BaseConfig:
	DEBUG = True
	HOST = '0.0.0.0'
	PORT = 8080

class DevelopmentConfig(BaseConfig):
	PORT = 5000

class ProductionConfig(BaseConfig):
	DEBUG = False
	PORT = 8000