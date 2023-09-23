from app.dao.dao import connect_database

def select_video_company(company_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT welcome_video_link, company_id from GamifiedJourney
	WHERE company_id = '{company_id}';
    """
    

    try:
        cursor.execute(query)
    except Exception as error:
        video_company = None
    else:
        video_company = cursor.fetchone()
    finally:
        connection.commit()
        connection.close()

    return video_company


def insert_video_company(company_id: int, link: str):
    
    connection, cursor = connect_database()
    
    video_exists = verify_video_company_exists(company_id)
    
    if video_exists:
        modify_video_company(company_id=company_id, new_link=link)
        return True

    
    query = f"""
    INSERT INTO GamifiedJourney
    (welcome_video_link, company_id) 
    VALUES 
    ('{link}', '{company_id}')
    ;
    """
    
    try:
        cursor.execute(query)
    except Exception as error:
        return False
    finally:
        connection.commit()
        connection.close()
        return True
    

def modify_video_company(company_id: int, new_link: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE GamifiedJourney
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
        
        return True


def delete_video(company_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE GamifiedJourney
	set welcome_video_link = ''
	WHERE company_id = '{company_id}';
    """
    
    
    try:
        cursor.execute(query)
    except:
        return None
    finally:
        connection.commit()
        connection.close()
        
        return True


def select_gamified_journey_id_by_company(company_id: int):

    connection, cursor = connect_database()

    query = f"""
    SELECT id FROM GamifiedJourney gj
    WHERE gj.company_id = {company_id};
    """

    try:
        cursor.execute(query)
    
    except Exception as error:
        connection.close()

        return None
    
    else:
        gamified_journey_id = cursor.fetchone()

        connection.close()

        return gamified_journey_id["id"]
    

def verify_video_company_exists(company_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT welcome_video_link, company_id from GamifiedJourney
	WHERE company_id = '{company_id}';
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    else:
        company_exists = cursor.fetchone()
        
        if company_exists:
            return True

    return False