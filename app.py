import asyncio
from database.database import MongoDB 
from db_model.product.product import Product
    
async def main():
    # Create the MongoDB connection
    db = MongoDB(db_name="Lonca")
    await db.connect()

    products = await Product.parse_xml_to_products('lonca-sample.xml')
    number_of_inserts,number_of_modifies = await db.upsert_products(products)

    if number_of_inserts != 0 or number_of_modifies != 0:
        print(f"{number_of_inserts} insert and {number_of_modifies} modify operations succesfully completed.")

if __name__ == "__main__":
    asyncio.run(main())