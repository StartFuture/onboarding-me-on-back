import logging

from app.dao.dao import connect_database

def select_company(company_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT * from Company
	WHERE id = '{company_id}';
    """

    try:
        cursor.execute(query)
    except Exception as error:
        company = None
        logging.error(f"error at select company: {error}")
    else:
        company = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()

    return company
