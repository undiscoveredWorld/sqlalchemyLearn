from pydantic import BaseModel


class ContractorBase(BaseModel):
    name: str
    description: str


class ContractorCreate(ContractorBase):
    pass


class ContractorUpdate(ContractorBase):
    id: int
    name: str | None
    description: str | None


class Contractor(ContractorBase):
    id: int

    class Config:
        from_attributes = True


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    id: int
    name: str | None


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class StorageBase(BaseModel):
    name: str
    description: str
    addr: str


class StorageCreate(StorageBase):
    pass


class StorageUpdate(StorageBase):
    id: int
    name: str | None
    description: str | None
    addr: str | None


class Storage(StorageBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    id: int


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class SellingDocumentBase(BaseModel):
    seller_id: int
    buyer_id: int
    product_id: int
    count: int
    cost: int


class SellingDocumentCreate(SellingDocumentBase):
    pass


class SellingDocumentUpdate(SellingDocumentBase):
    id: int
    seller_id: int | None
    buyer_id: int | None
    product_id: int | None
    count: int | None
    cost: int | None


class SellingDocument(SellingDocumentBase):
    id: int

    class Config:
        from_attributes = True
