from app.dao.dao import connect_database

def select_company(company_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT * from Company
	WHERE id = '{company_id}';
    """

    try:
        cursor.execute(query)
    except:
        company = None
    else:
        company = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()

    return company
