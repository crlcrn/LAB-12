from database.DB_connect import DBConnect
from model.Retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNation():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct Country 
                from go_retailers gr 
                order by Country asc 
                """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodi(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct gr.*
                from go_retailers gr 
                where gr.Country = %s
                """

        cursor.execute(query, (country, ))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi(year, country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select gr1.Retailer_code as g1, gr2.Retailer_code as g2, count(distinct s1.Product_number) as peso 
                from go_retailers gr1, go_retailers gr2, go_daily_sales s1, go_daily_sales s2
                where year(s1.`Date`) = year(s2.`Date`)
                and year(s1.`Date`) =  %s
                and gr1.Country = %s and gr2.Country = %s
                and gr2.Retailer_code = s2.Retailer_code and gr1.Retailer_code = s1.Retailer_code 
                and s2.Product_number = s1.Product_number and gr1.Retailer_code < gr2.Retailer_code
                GROUP BY gr1.Retailer_code, gr2.Retailer_code
                """

        cursor.execute(query, (year, country, country,  ))

        for row in cursor:
            result.append((row['g1'], row['g2'], row['peso']))

        cursor.close()
        conn.close()
        return result
