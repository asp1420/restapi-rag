from base64 import b64encode
from fastapi import APIRouter, status, UploadFile, HTTPException
from ..worker import process_data
from ..consts.stypes import Services
from ..consts.api import DOC_ADD_COLLECTION, DOC_QUERY_DB
from ..schemas.rag import RequestResponse


router = APIRouter(
    tags=['Transcribe'],
    responses={
        status.HTTP_404_NOT_FOUND: {'description': 'Go to /docs for more information'}
    }
)


@router.post(
    path='/api/document',
    summary=DOC_ADD_COLLECTION,
    response_model=RequestResponse,
    response_model_exclude_unset=True,
    status_code=status.HTTP_202_ACCEPTED
)
async def add_document(document: UploadFile | None, collection: str) -> RequestResponse:
    if not document:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='')
    data_bytes = await document.read()
    data_type = document.content_type
    filename = document.filename
    bytes64 = b64encode(data_bytes)
    base64_string = bytes64.decode('utf-8')
    result, details = process_data(
        service=Services.ADD_DOCUMENT, data_bytes=base64_string,
        data_type=data_type, filename=filename, collection=collection
    )
    request_details = {'response': result}
    if details is not None:
        request_details.update({'details': details})
    response =  RequestResponse(**request_details)
    return response


@router.post(
    path='/api/query',
    summary=DOC_QUERY_DB,
    response_model=RequestResponse,
    response_model_exclude_unset=True,
    status_code=status.HTTP_202_ACCEPTED
)
async def query_from_db(query: str, collection: str | None=None) -> RequestResponse:
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='')
    result, details = process_data(
        service=Services.QUERY_DB, data_bytes=query,
        collection=collection
    )
    request_details = {'response': result}
    if details is not None:
        request_details.update({'details': details})
    response =  RequestResponse(**request_details)
    return response
