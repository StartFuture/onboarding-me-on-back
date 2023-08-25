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


def get_company_id(quiz_id: int = None, tool_id: int = None):

    connection, cursor = connect_database()

    if quiz_id:
        query = f"""
        SELECT c.id FROM Quiz q LEFT JOIN Game g ON q.game_id = g.id LEFT JOIN GamifiedJourney gj ON g.gamified_journey_id = gj.id
        LEFT JOIN Company c ON gj.company_id = c.id
        WHERE q.id = {quiz_id};
        """
    else:
        query = f"""
        SELECT c.id FROM Tool t LEFT JOIN Game g ON t.game_id = g.id LEFT JOIN GamifiedJourney gj ON g.gamified_journey_id = gj.id
        LEFT JOIN Company c ON gj.company_id = c.id
        WHERE t.id = {tool_id};
        """
    
    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return None
    else:
        company_id = cursor.fetchone()

        connection.close()

        return company_id["id"]


def verify_if_company_exists(company_id: int):
    
    connection, cursor = connect_database()
    
    query =f"""
    SELECT id
    FROM Company
    WHERE id = {company_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False    
    
    else:    
        
        company_exists = cursor.fetchone()
        connection.close()
        
        if company_exists:
            return True
        
    return False