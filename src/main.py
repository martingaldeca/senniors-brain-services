import pandas as pd
import uvicorn
import logging.config
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

import settings
from brain_services.predictor import SenniorsPredictor
from celery_brain_services.celery import task_train_and_select_pipelines
from settings import API_KEY
from pydantic import BaseModel
from security import api_key_auth

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI(
    title='Senniors brain-services',
    docs_url=settings.DOCS_URL if settings.DOCS_URL != 'None' else None,
    redoc_url=settings.REDOC_URL if settings.REDOC_URL != 'None' else None
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=API_KEY)


class PostedData(BaseModel):
    gender: int = None
    scheduled_day: str = None
    appointment_day: str = None
    age: int = None
    neighbourhood: str = None
    scholarship: int = None
    hypertension: int = None
    diabetes: int = None
    alcoholism: int = None
    handicap: int = None
    sms_received: int = None


class PredictionResult(BaseModel):
    attending: bool = None


@app.get('/ping')
async def ping():
    """
    Ping endpoint to check that the service is up
    :return:
    """
    return 'pong'


@app.post('/train_pipelines', dependencies=[Security(api_key_auth)])
async def train_pipelines():
    logger.info('The pipelines will be trained in an asynchronous process')
    task_train_and_select_pipelines.delay()
    return 'Training pipelines'


@app.post('/predict_attending', dependencies=[Security(api_key_auth)], response_model=PredictionResult)
async def predict_attending(posted_notification: PostedData):
    """
    Main endpoint, it will return a prediction of the value of no-show for a customer from some data

    :param posted_notification:
    :return: dict with the result that shows if the customer will attend to the hospital
    """
    try:
        predictor = SenniorsPredictor()
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail='There is not a valid pipeline, please wait until it is trained or call the train_pipelines endpoint'
        )
    x = pd.DataFrame(posted_notification.__dict__, index=[0])
    try:
        result = predictor.predict(x)
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail={
                'message': 'There was a problem with the prediction',
                'exception': ex
            }
        )
    return {'attending': result}


if __name__ == "__main__":
    # Test purposes
    if settings.ENVIRONMENT == 'local':
        uvicorn.run(app, host="0.0.0.0", port=settings.DEBUGGING_PORT)
    else:
        logger.warning('Only available for local environments')
