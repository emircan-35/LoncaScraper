import asyncio, os

from database.database import MongoDB 
from db_model.product.product import Product
from dotenv import load_dotenv
    
async def main():
    load_dotenv() 

    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = int(os.getenv("DB_PORT"))

    db = MongoDB(DB_NAME,DB_PORT)

    await db.connect()

    products = await Product.parse_xml_to_products('lonca-sample.xml')
    number_of_inserts,number_of_modifies = await db.upsert_products(products)

    if number_of_inserts != 0 or number_of_modifies != 0:
        print(f"{number_of_inserts} insert and {number_of_modifies} modify operations succesfully completed.")

if __name__ == "__main__":
    asyncio.run(main())