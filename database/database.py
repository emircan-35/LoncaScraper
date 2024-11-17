import logging

from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydantic import BaseModel
from typing import List
from db_model.product.product import Product

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self, db_name: str, host: str = "localhost", port: int = 27017):
        """ Initializes the connection to MongoDB """
        self.db_name = db_name
        self.host = host
        self.port = port
        self.client = None
        self.db = None

    async def connect(self):
        """ Connect to MongoDB and initialize the Beanie models """
        self.client = AsyncIOMotorClient(self.host, self.port)
        self.db = self.client[self.db_name]
        
        await init_beanie(self.db, document_models=[Product])


    async def upsert_products(self, products: List[Product]):
        """
        Insert or update products based on stock_code.
        
        Args:
            products (List[Product]): List of Product instances to be inserted/updated.
        
        Returns:
            int: The number of upsert operations performed.
        """
        operations = []
        for product in products:
            product_dict = product.model_dump(by_alias=True, exclude_unset=True)  

            operations.append(
                UpdateOne(
                    {"stock_code": product.stock_code}, 
                    {"$set": product_dict},  
                    upsert=True  
                )
            )
        
        try:
            result = await Product.get_motor_collection().bulk_write(operations)
            return (result.upserted_count, result.modified_count)  

        except BulkWriteError as e:
            print(f"Error occurred during bulk write operation: {e.details}")
            return 0
