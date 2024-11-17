import asyncio
from database.database import MongoDB 
from db_model.product.product import Product
    
async def main():
    # Create the MongoDB connection
    db = MongoDB(db_name="Lonca")
    await db.connect()

    products = await Product.parse_xml_to_products('C:/Users/emirc/OneDrive/Masaüstü/lonca/lonca-sample.xml')
    await db.upsert_products(products)

if __name__ == "__main__":
    asyncio.run(main())