from typing import List
from beanie import Document
from enum import Enum
from lxml import etree
from datetime import datetime
from pydantic import Field
from typing import Optional

from pydantic_core import ValidationError

class Color(str, Enum):
    BEJ = "Bej"
    TURUNCU = "Turuncu"
    RED = "Red"
    BLUE = "Blue"
    GREEN = "Green"
    SARI = "Sarı"
    EKRU = "Ekru"
    VIZON = "Vizon"

class Product(Document):
    stock_code: str = Field(..., alias="stockCode")
    color: List[Color] = Field(..., alias="color")
    discounted_price: float = Field(..., alias="discountedPrice")
    images: List[str] = Field(..., alias="images")
    is_discounted: bool = Field(..., alias="isDiscounted")
    name: str = Field(..., alias="name")
    price_unit: Optional[str] = Field(..., alias="priceUnit")
    product_type: str = Field(..., alias="productType")
    quantity: int = Field(..., alias="quantity")
    sample_size: Optional[str] = Field(None, alias="sampleSize")
    series: str = Field(..., alias="series")
    status: Optional[str] = Field(None, alias="status")
    fabric: Optional[str] = Field(None, alias="fabric")
    model_measurements: Optional[str] = Field(None, alias="modelMeasurements")
    product_measurements: Optional[str] = Field(None, alias="productMeasurements")
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: datetime = Field(..., alias="updatedAt")

    class Settings:
        collection = "products"

    @staticmethod
    async def parse_xml_to_products(xml_path: str) -> List["Product"]:
        tree = etree.parse(xml_path)
        root = tree.getroot()

        products = []

        for product_element in root.findall(".//Product"):
            images = [img.get("Path") for img in product_element.findall("Images/Image") if img.get("Path")]

            product_details = {detail.get("Name"): detail.get("Value") for detail in product_element.findall("ProductDetails/ProductDetail")}

            try:
                product = Product(
                    stock_code = product_element.get("ProductId", None),
                    name = product_element.get("Name", None),
                    color = [Color(c) for c in product_details.get("Color", "").split(",")] if "Color" in product_details else [],
                    images = images,
                    is_discounted = product_details.get("DiscountedPrice", "0") != "0",
                    discounted_price = float(product_details.get("DiscountedPrice", "0").replace(",", ".")) if product_details.get("DiscountedPrice") else None,
                    price = float(product_details.get("Price", "0").replace(",", ".")) if product_details.get("Price") else None,
                    price_unit = product_details.get("PriceUnit", None),
                    product_type = product_details.get("ProductType", None),
                    quantity = int(product_details.get("Quantity", None)),
                    sample_size = product_details.get("SampleSize", None),
                    series = product_details.get("Series", None),
                    status = product_details.get("Status", None),
                    fabric = product_details.get("Fabric", None),
                    model_measurements = product_details.get("ModelMeasurements", None),
                    product_measurements = product_details.get("ProductMeasurements", None),
                    createdAt = datetime.utcnow(),
                    updatedAt = datetime.utcnow()
                )
                products.append(product)
            except ValidationError as err:
                print("Validation error occured for one or more following fields.")
                print(etree.tostring(product_element, pretty_print=True).decode())
                print("Continue with the next element...")

        return products
