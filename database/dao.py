from database.DB_connect import DBConnect
from model.categories import Category
from model.products import Product


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_categories():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM category """

        cursor.execute(query)

        for row in cursor:
            result.append(Category(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodes(category_id: int):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM product 
         WHERE category_id = %s"""

        cursor.execute(query, (category_id,))

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_all_products():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM product 
             WHERE category_id = %s"""

        cursor.execute(query)

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_sales(data_inizio, data_fine):
        conn = DBConnect.get_connection()

        sale= []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT oi.product_id, count(oi.order_id) as num_vendite 
                    FROM order_item oi, `order` o
                    where oi.order_id=o.id
                    and o.order_date between %s and %s
                    group by oi.product_id"""

        cursor.execute(query, (data_inizio, data_fine))

        for row in cursor:
            sale.append((row["product_id"], row["num_vendite"]))

        cursor.close()
        conn.close()
        return sale