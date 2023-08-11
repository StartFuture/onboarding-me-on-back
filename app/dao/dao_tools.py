from app.dao.dao import connect_database
from app.schemas.tool import Tool
from app.schemas.category_tool import CategoryTool


def select_tools(id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT t.name, t.score FROM Tool t
    left join Game g on g.id = t.game_id 
    left join GamifiedJourney gj on gj.id = g.gamified_journey_id 
    left join Company c on c.id = gj.company_id 
    WHERE
    c.id ={id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
        
    else:    
        tool_list = cursor.fetchall()
        connection.close()

        return tool_list


def select_category_tool(id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT ct.name FROM CategoryTool ct 
    left join Tool t on t.id = ct.id 
    WHERE t.id = {id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        category_tool_list = cursor.fetchone()
        connection.close()
        
        return category_tool_list


def insert_category_tool(category_tool: CategoryTool):
    
    connection, cursor = connect_database()
    
    query = f"""
    INSERT INTO CategoryTool 
    (name)
    VALUES
    ('{category_tool.name}')
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        connection.commit()
        
        query = f'SELECT LAST_INSERT_ID() FROM CategoryTool;'
        cursor.execute(query)
        
        category_tool_id = cursor.fetchone()
        connection.close()

        return category_tool_id


def verify_if_category_exists(category_tool: CategoryTool):
    
    connection, cursor = connect_database()
    
    query =f"""
    SELECT name From CategoryTool ct WHERE name = '{category_tool.name}'
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False    
    
    else:    
        
        category_exists = cursor.fetchone()
        connection.close()
        
        if category_exists:
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
    