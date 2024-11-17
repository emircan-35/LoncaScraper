from typing import List
from beanie import Document
from enum import Enum
from lxml import etree
from datetime import datetime
from pydantic import Field
from typing import Optional

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
    price: float = Field(..., alias="price")
    price_unit: str = Field(..., alias="priceUnit")
    product_type: str = Field(..., alias="productType")
    quantity: int = Field(..., alias="quantity")
    sample_size: Optional[str] = Field(None, alias="sampleSize")
    series: str = Field(..., alias="series")
    status: Optional[str] = Field(None, alias="status")
    fabric: Optional[str] = Field(None, alias="fabric")
    model_measurements: Optional[str] = Field(None, alias="modelMeasurements")
    product_measurements: Optional[str] = Field(None, alias="productMeasurements")
    createdAt: datetime = Field(..., alias="createdAt")
    updatedAt: Optional[datetime] = Field(..., alias="updatedAt")

    class Settings:
        collection = "products"  

    @staticmethod
    def safe_find(element, tag, transform_func=str, default=None):
        """
        Helper function to find an element and apply a transformation function.
        Returns a default value if the element is not found or can't be transformed.
        """
        found_element = element.find(tag)
        if found_element is not None and found_element.text:
            try:
                return transform_func(found_element.text)
            except ValueError:
                return default  # Return default value in case of a transformation error
        return default

    @staticmethod
    async def parse_xml_to_products(xml_path: str) -> List["Product"]:
        tree = etree.parse(xml_path)
        root = tree.getroot()

        products = []

        for product_element in root.findall(".//Product"):
            images = [img.get("Path") for img in product_element.findall("Images/Image") if img.get("Path")]

            product_details = {detail.get("Name"): detail.get("Value") for detail in product_element.findall("ProductDetails/ProductDetail")}

            product = Product(
                stock_code=product_element.get("ProductId", ""),
                name=product_element.get("Name", ""),
                color=[Color(c) for c in product_details.get("Color", "").split(",")] if "Color" in product_details else [],
                discounted_price=Product.safe_find(product_element, "ProductDetails/ProductDetail[@Name='DiscountedPrice']", transform_func=lambda x: float(x.replace(",", ".")), default=0.0),
                images=images,
                is_discounted=Product.safe_find(product_element, "ProductDetails/ProductDetail[@Name='DiscountedPrice']", transform_func=lambda x: float(x.replace(",", ".")) > 0, default=False),
                price=Product.safe_find(product_element, "ProductDetails/ProductDetail[@Name='Price']", transform_func=lambda x: float(x.replace(",", ".")), default=0.0),
                price_unit="",  
                product_type=product_details.get("ProductType", ""),
                quantity=int(product_details.get("Quantity", 0)),
                sample_size=product_details.get("SampleSize", ""),  
                series=product_details.get("Series", ""),
                status=product_details.get("Status", None),  
                fabric=product_details.get("Fabric", None),  
                model_measurements=product_details.get("ModelMeasurements", None), 
                product_measurements=product_details.get("ProductMeasurements", None),  
                createdAt=datetime.utcnow(),  
                updatedAt=None  
            )
            products.append(product)

        return products
