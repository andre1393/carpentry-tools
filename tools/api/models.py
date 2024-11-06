from pydantic import BaseModel
from typing import List, Union


class Item(BaseModel):
    name: str
    description: str
    quantity: int
    unit_price: float
    total: str = None


class QuoteParams(BaseModel):
    in_cash_discount_rate: float = .1
    company_name: str = "Ronaldo Restauração de móveis e Marcenária"
    date: str = None
    project_description: str
    client_name: str
    items: List[Item]
    num_instalments: int = 3
    include_material: bool = True
    include_shipping: bool = True
    in_cash_total: str = None
    total: str = None
    quote_includes: str = None


class GoogleDriveInput(BaseModel):
    doc_id: str


class LocalFileInput(BaseModel):
    base_dir: str
    file_name: str


class LocalFileOutput(BaseModel):
    base_dir: str
    file_name: str = None


class GoogleDriveOutput(BaseModel):
    tmp_dir: str = "/tmp"
    file_name: str = None
    parent_dir_id: str


class DocumentInput(BaseModel):
    type: str
    params: Union[GoogleDriveInput, LocalFileInput]


class DocumentOutput(BaseModel):
    type: str
    params: Union[GoogleDriveOutput, LocalFileOutput]


class RequestParams(BaseModel):
    quote_params: QuoteParams
    doc_input: DocumentInput
    doc_output: DocumentOutput
