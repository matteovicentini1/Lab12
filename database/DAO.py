from database.DB_connect import DBConnect
from model.Retailer import Retailer

class DAO():
    @staticmethod
    def getCountry():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gr.Country as c
from go_retailers gr 
order by c asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row['c'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRivenditori(y):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers gr 
                    where gr.Country =%s 
                    """

        cursor.execute(query,(y,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getarchi(naz,year,id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.Retailer_code as r1,t2.Retailer_code as r2, count(distinct t1.Product_number)as peso 
                    from (select gds.Retailer_code ,gds.Product_number 
		                    from go_daily_sales gds 
		                    where year(gds.`Date`)=%s and gds.Retailer_code =%s) as t1,
	(select gds.Retailer_code ,gds.Product_number 
		from go_daily_sales gds 
		where year(gds.`Date`)=%s and gds.Retailer_code in (select gr.Retailer_code
                from go_retailers gr 
                where gr.Country =%s )) as t2
where t1.Retailer_code != t2.Retailer_code and t1.Product_number=t2.Product_number
group by r1,r2
                        """

        cursor.execute(query, (year,id,year,naz,))

        for row in cursor:
            result.append((row['r1'],row['r2'],row['peso']))

        cursor.close()
        conn.close()
        return result
