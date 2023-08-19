from app.dao.dao import connect_database

def select_video_company(company_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT welcome_video_link, company_id from GamifiedJourney
	WHERE company_id = '{company_id}';
    """

    try:
        cursor.execute(query)
    except:
        video_company = None
    else:
        video_company = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()

    return video_company


def insert_video_company(company_id: int, link: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    INSERT INTO GamifiedJourney(welcome_video_link, company_id) VALUES ('{link}', '{company_id}');
    """
    try:
        print(query)
        cursor.execute(query)
    except TypeError:
        print(query)
        return TypeError
    finally:
        connection.commit()
        connection.close()

def modify_video_company(company_id: int, new_link: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE GamifiedJourney(welcome_video_link, company_id)
	set welcome_video_link = '{new_link}'
	WHERE company_id = '{company_id}';
    """
    
    try:
        cursor.execute(query)
    except:
        return None
    finally:
        connection.commit()
        connection.close()
