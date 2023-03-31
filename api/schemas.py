from ninja import ModelSchema, Field, Schema, File
# from ninja.files import UploadedFile
from typing import List, Optional
from .models import CakeOrder, CatalogCake


# Cake
class UpdateCustomCakeSchema(Schema):
    language: str
    order_id: int
    inside: str = None
    cakebatter: str = None
    outside_content: str = None
    outside_colour: str = None
    persons: int = None
    form: str = None
    floors: int = None
    deko: List[str] = None
    text: str = None
    text_material: str = None
    deadline_time: str = None
    deadline_date: str = None
    customer_name: str = None
    customer_surname: str = None
    customer_phone: str = None
    customer_mail: str = None
    customer_info: str = None
    shop_assistant_order: str = None
    shop_assistant_info: str = None
    price: float = None


class CakeOrderModelSchema(ModelSchema):
    class Config:
        model = CakeOrder
        model_fields = '__all__'


class CakeOrderSchema(Schema):
    language: str
    cake_model: str = None
    inside: str
    cakebatter: str
    outside_content: str
    outside_colour: str
    persons: int
    form: str
    floors: int
    deko: List[str] = None
    text: str = None
    text_material: str = None
    deadline_time: str
    deadline_date: str
    customer_name: str
    customer_surname: str
    customer_phone: str = None
    customer_info: str = None
    customer_mail: str = None
    shop_assistant_order: str
    shop_assistant_info: str = None
    price: float = None


class CatalogCakeSchema(Schema):
    cake_nr: int
    name: str
    description: str
    inside: str
    cakebatter: str
    outside_content: str
    outside_colour: str
    persons: int
    form: str
    floors: int
    deko: List[str] = None
    price: float = None


class CatalogCakeModelSchema(ModelSchema):
    class Config:
        model = CatalogCake
        model_fields = '__all__'