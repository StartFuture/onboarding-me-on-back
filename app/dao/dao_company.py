from io import BytesIO, StringIO

from app.dao.dao import connect_database
from app.schemas.company import Company


def select_company(company_id: int):
    
    connection, cursor = connect_database()
    
        
    query = f"""
    SELECT c.company_name, c.trading_name, c.cnpj, c.company_password, c.state_register 
    from Company c 
    WHERE id = {company_id}
    ;
    """


    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        company = cursor.fetchone()
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
    

def insert_company(company: Company):
    
    connection, cursor = connect_database()
    
    query ="""
    INSERT INTO Company
    (company_name, trading_name, logo, cnpj, email, company_password, state_register)
    VALUES
    (%s, %s, %s, %s, %s, %s, %s);
    """
    
    params = (company.name, company.trading_name, company.logo, company.cnpj, company.email, company.password, company.state_register)
    
    try:
        cursor.execute(query, params)

    except Exception as error:
        connection.close()
        return False

    else:
        connection.commit()
        connection.close()
        return True
    
    
    
    
    
    
    
    
    
    

def verify_company_exists_by_email(company_email: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT email
    FROM Company c 
    WHERE c.email = '{company_email}';
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        user_exists = cursor.fetchone()
        connection.close()
        if user_exists:
            return True
        
        return False


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