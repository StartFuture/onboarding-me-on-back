from app.dao.dao import connect_database
from app.schemas.employee import FeedBackEmployee


def select_feedback_company(company_id: int):
    
    connection, cursor = connect_database()

    query = f"""
    SELECT ef.employee_id, ef.grade,ef.message, ef.feedback_type FROM Employee_Feedback ef
    LEFT JOIN Employee e ON e.id = ef.employee_id 
    LEFT JOIN Company c ON c.id = e.company_id 
    WHERE c.id = {company_id}
    ;
    """
    
    try:
        cursor.execute(query)
    except Exception as error:
        connection.close()
        return None
    else:
        feedback_list =  cursor.fetchall()
        connection.close()
        return feedback_list

def insert_feedback(feedback_employee: FeedBackEmployee):
    connection, cursor = connect_database()

    query = f"""
    INSERT INTO onboarding_me.Employee_Feedback
    (employee_id, grade, message, feedback_type)
    VALUES({feedback_employee.employee_id}, {feedback_employee.grade}, '{feedback_employee.message}', '{feedback_employee.feedback_type}');
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