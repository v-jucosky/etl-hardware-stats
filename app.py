from sqlalchemy import MetaData, Table, Column, Integer, Float, DateTime, create_engine
from datetime import datetime
from time import time, sleep


import psutil
import os


DB_CREDENTIALS = {
    'schema': 'RASPBERRY',
    'host': '192.168.0.10',
    'port': '3306',
    'user': str(os.environ['sql_uid']),
    'password': str(os.environ['sql_pwd']),
}

INTERVAL = 2.0


class HardwareMonitor():
    global DB_CREDENTIALS

    def __init__(self):
        metadata = MetaData()
        engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(
                            DB_CREDENTIALS['user'], DB_CREDENTIALS['password'],
                            DB_CREDENTIALS['host'], DB_CREDENTIALS['port'],
                            DB_CREDENTIALS['schema']))

        self.rpi_cpu_usage = Table(
            'rpi_cpu_usage', metadata,
            Column('id', Integer, primary_key=True, nullable=False), 
            Column('usage', Float),
            Column('current_freq', Float),
            Column('minimum_freq', Float),
            Column('maximum_freq', Float),
            Column('date', DateTime, default=datetime.now),
        )
        self.rpi_mem_usage = Table(
            'rpi_mem_usage', metadata,
            Column('id', Integer, primary_key=True, nullable=False), 
            Column('usage', Integer),
            Column('total', Integer),
            Column('available', Integer),
            Column('used', Integer),
            Column('free', Integer),
            Column('date', DateTime, default=datetime.now),
        )

        metadata.create_all(engine)
        self.connection = engine.connect()

    def collect_data(self):
        cpu_load = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq()
        mem_load = psutil.virtual_memory()

        self.connection.execute(
            self.rpi_cpu_usage.insert().values(
                usage=cpu_load,
                current_freq=cpu_freq[0],
                minimum_freq=cpu_freq[1],
                maximum_freq=cpu_freq[2],
            )
        )
        self.connection.execute(
            self.rpi_mem_usage.insert().values(
                usage=mem_load[2],
                total=mem_load[0] / 2**20,
                available=mem_load[1] / 2**20,
                used=mem_load[3] / 2**20,
                free=mem_load[4] / 2**20,
            )
        )


if __name__ == '__main__':
    start = time()
    hardware_monitor = HardwareMonitor()
    while True:
        hardware_monitor.collect_data()
        sleep(INTERVAL - ((time() - start) % INTERVAL))
else:
    raise EnvironmentError