
from .app_config import app

from .flows import FlowSample
from .consumers import print_smth


@app.pipeline()
def main(pipeline, data_frame):
    return data_frame\
        .rename(data=data_frame)\
        .subscribe_flow(FlowSample())\
        .subscribe_consumer(print_smth)



