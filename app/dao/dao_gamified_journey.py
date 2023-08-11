from app.dao.dao import connect_database

def select_video_company(id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT welcome_video_link, company_id from GamifiedJourney
	WHERE id = '{id}';
    """

    try:
        cursor.execute(query)
    except:
        video_company = None
    else:
        video_company = cursor.fetchone()
    finally:
        connection.close()

    return video_company


def insert_video_company(id: int, link: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    insert into GamifiedJourney(welcome_video_link, company_id ) values ({link},{id});
    """
    try:
        cursor.execute(query)
    except:
        None
    finally:
        connection.commit()
        connection.close()

def modify_video_company(id: int, new_link: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE GamifiedJourney(welcome_video_link, company_id )
	set welcome_video_link = '{new_link}'
	WHERE company_id = '{id}';
    """
    
    try:
        cursor.execute(query)
    except:
        None
    finally:
        connection.commit()
        connection.close()
