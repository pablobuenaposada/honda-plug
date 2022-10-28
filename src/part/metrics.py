from prometheus_client import Gauge

parts = Gauge("parts", "number of total parts")
stocks = Gauge("stocks", "number of total stocks")
images = Gauge("images", "number of total images")
