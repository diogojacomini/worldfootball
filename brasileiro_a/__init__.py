import logging
from azure.functions import HttpRequest, HttpResponse

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    return HttpResponse("Hello, world!")
