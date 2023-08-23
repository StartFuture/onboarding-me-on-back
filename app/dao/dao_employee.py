from app.dao.dao import connect_database


def get_employee_answer(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT a.is_answer, q.score as quiz_score FROM Employee e 
    left join Employee_Alternative ea on ea.employee_id = e.id 
    left join Alternative a on a.id = ea.alternative_id 
    left join Quiz q on q.id  = a.quiz_id 
    WHERE e.id = {employee_id};
    ;
    """
    
    try:
        cursor.execute(query)

    except Exception as error:
        connection.close()
        return None

    else:

         data_list = cursor.fetchall()
         connection.close()

         return data_list
    
    
def insert_employee_score(employee_id: int):
    
    connection, cursor = connect_database()
    
    data_list = get_employee_answer(employee_id= employee_id)
    
    for data_dict in data_list:
        is_answer = data_dict['is_answer']
        score = data_dict['quiz_score']
    
    if is_answer == 1:
        
        query = f"""
        INSERT INTO Score
        (total_points, employee_id)
        VALUES
        ({score}, {employee_id})
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
          
    return False
        
        
def get_total_score(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT total_points 
    FROM Score
    WHERE employee_id = {employee_id}
    ;
    """
    
    try:
        cursor.execute(query)

    except Exception as error:
        connection.close()
        return None

    else:

         list_score = cursor.fetchall()
         total_score = 0
         
         for point in list_score:
             total_score += point['total_points']
         
         
         connection.close()
         return total_score    
        
        
def verify_employee_exists(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id
    FROM onboarding_me.Employee
    WHERE id = {employee_id}
    ;
    """
    
    try:
        cursor.execute(query)

    except Exception as error:
        connection.close()
        return None

    else:

         employee_exists = cursor.fetchone()
         
         if employee_exists:
             return True
    
    return False
        
