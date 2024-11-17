import logging

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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
        
        # Initialize Beanie with the Product model
        await init_beanie(self.db, document_models=[Product])

    async def insert_one(self, product: Product) -> str:
        """ Insert a single product document into the Products collection """
        try:
            await product.insert()
            return str(product.id)  # Return the product's ID as a string
        except Exception as e:
            logger.error(f"Error inserting product: {e}")
            return ""

    async def add_many(self, products: List[Product]) -> None:
        """
        Insert multiple Product documents into the database.

        Args:
            products (List[Product]): List of Product instances to be inserted.
        """
        try:
            await Product.insert_many(products)
        except Exception as e:
            logger.error(f"Error inserting multiple products: {e}")

    async def find_one(self, query: Dict[str, Any]) -> Optional[Product]:
        """ Find a single document based on a query """
        try:
            return await Product.find_one(query)
        except Exception as e:
            logger.error(f"Error finding product: {e}")
            return None
