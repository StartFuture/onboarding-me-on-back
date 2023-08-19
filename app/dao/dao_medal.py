from app.dao.dao import connect_database

def select_medal(medal_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT image, medal_id from Medal
	WHERE medal_id = '{medal_id}';
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
    INSERT INTO Medal(image, medal_id) VALUES ('{medal_image}','{medal_id}');
    set image = '{medal_image}'
	WHERE medal_id = '{medal_id}';
    """
    
    try:
        cursor.execute(query)
    except:
        None
    finally:
        connection.commit()
        connection.close()

def modify_medal(medal_id: int, medal_image: blob):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE Medal(image, medal_id) 
    set image = '{medal_image}'
	WHERE medal_id = '{medal_id}';
    """
    
    try:
        cursor.execute(query)
    except:
        None
    finally:
        connection.commit()
        connection.close()
