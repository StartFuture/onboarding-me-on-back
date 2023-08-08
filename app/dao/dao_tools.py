from app.dao.dao import connect_database
from app.schemas.category_tool import CategoryTool


def select_tool(id: int):
    
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

    cursor.execute(query)
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

    cursor.execute(query)
    category_tool_list = cursor.fetchone()
    connection.close()
    
    return category_tool_list


def insert_category_tool(category_tool: CategoryTool):
    
    connection, cursor = connect_database()
    
    query = f"""
    INSERT INTO CategoryTool 
    (name)
    VALUES
    ('{category_tool.name}');
    """

    cursor.execute(query)
    connection.commit()
    
    query = f'SELECT name FROM CategoryTool WHERE name = "{category_tool.name}"'

    cursor.execute(query)
    category_tool_list = cursor.fetchone()
    connection.close()

    return category_tool_list


def verify_category_exists(category_tool: CategoryTool):
    
    connection, cursor = connect_database()
    
    query =f"""
    SELECT name From CategoryTool ct WHERE name = '{category_tool.name}';
    """
    
    cursor.execute(query)
    category_exists = cursor.fetchone()
    
    if category_exists:
        return True
    
    return False
    
    