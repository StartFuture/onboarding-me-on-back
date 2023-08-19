from app.dao.dao import connect_database

def select_medal(medal_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT image, medal_id from Medal
	WHERE id = '{id}';
    """

    try:
        cursor.execute(query)
    except:
        image = None
    else:
        image = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()


def insert_medal(medal_id: int, medal_image: blob):
    
    connection, cursor = connect_database()
    
    query = f"""
    insert into Medal(image) values ({medal_image},{medal_id});
    set image = '{medal}'
	WHERE medal_id = '{id}';
    """
    try:
        cursor.execute(query)
    except:
        None
    finally:
        connection.commit()
        connection.close()

def insert_medal(medal_id: int, new_link: str):
    
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
