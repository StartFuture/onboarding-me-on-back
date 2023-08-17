from app.dao.dao import connect_database
from app.schemas.tool import Tool, EmployeeTool
from app.schemas.category_tool import CategoryTool


def select_tools(id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT t.name, t.link_download, t.score FROM Tool t
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
    


def insert_tool(tool: Tool):

    connection, cursor = connect_database()

    query = f"""
    INSERT INTO Tool 
    (link_download, name, score, game_id, category_id)
    VALUES
    ('{tool.link_download}', '{tool.name}', {tool.score}, {tool.game_id}, {tool.category_id});
    """
    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    else:
        connection.commit()
        connection.close()

        return True
    

def update_tool(tool: Tool):

    connection, cursor = connect_database()

    query = f"""
    UPDATE Tool
    SET link_download = '{tool.link_download}', name = '{tool.name}', score = {tool.score}, category_id = {tool.category_id} 
    WHERE id = {tool.id_tool};
    """
    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    else:
        connection.commit()
        connection.close()

        return True


def delete_tool(tool_id : int, game_id: int):

    connection, cursor = connect_database()

    query = f"""
    DELETE FROM Tool
    WHERE game_id = {game_id} and id= {tool_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False

    else:
        
        connection.commit()
        connection.close()
    
        return True   
    
    
def verify_tool_exists(name: str = None, id_tool: int = None):

    connection, cursor = connect_database()

    if id_tool:
        query = f"SELECT id FROM Tool WHERE id = {id_tool}"
    else:
        query = f"SELECT id FROM Tool WHERE name = {name}"
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        tool_id = cursor.fetchone()

        connection.close()

        return bool(tool_id)


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

def update_category_tool(category_tool: CategoryTool):
    
    connection, cursor = connect_database()
    
    query = f"""
    UPDATE CategoryTool
    SET name = '{category_tool.name}'
    WHERE id = {category_tool.category_tool_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        
        connection.commit()
        connection.close()

        return True
    
    
def delete_category_tool(category_tool_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT t.id FROM onboarding_me.CategoryTool ct
    left join Tool t on t.category_id = ct.id
    WHERE ct.id= {category_tool_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        
        list_tools_id = cursor.fetchall()
        ids = [tool['id'] for tool in list_tools_id]
 
        placeholder = ','.join(['%s'] * len(ids))
        
        query = f"""
        DELETE FROM Tool  
        WHERE category_id = %s AND id IN ({placeholder});
        ;
        """
        
        try:
            cursor.execute(query, [category_tool_id] + ids)
            
        except Exception as error:
            connection.close()
            return False
        
        else:
            
            query = f"""
            DELETE FROM CategoryTool
            WHERE id = {category_tool_id}
            ;
            """

            try:
                cursor.execute(query)
                
            except Exception as error:
                connection.close()
                return False

            else:
                
                connection.commit()
                connection.close()

                return True
    

def verify_if_category_exists(category_name: str = None, category_id: int = None):
    
    connection, cursor = connect_database()
    
    if category_name:
    
        query =f"""
        SELECT name From CategoryTool ct WHERE name = '{category_name}'
        ;
        """
        
    if category_id:
        
        query =f"""
        SELECT id From CategoryTool ct WHERE id = '{category_id}'
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


def linking_tool(employee_tool: EmployeeTool):

    connection, cursor = connect_database()

    query = f"""
    INSERT INTO Employee_Tool (employee_id, tool_id, nick_name)
    VALUES ({employee_tool.employee_id}, {employee_tool.tool_id}, '{employee_tool.nick_name}');
    """

    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    else:
        connection.commit()
        connection.close()

        return True


def verify_tool_completed(tool_id: int = None, employee_tool_id: int = None):

    connection, cursor = connect_database()

    if employee_tool_id:
        query = f"SELECT id FROM Employee_Tool WHERE id = {employee_tool_id}"
    else:
        query = f"SELECT id FROM Employee_Tool WHERE tool_id = {tool_id}"
    
    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return False
    else:
        tool_id = cursor.fetchone()

        connection.close()

        return bool(tool_id)