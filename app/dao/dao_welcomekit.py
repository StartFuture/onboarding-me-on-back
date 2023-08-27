from app.dao.dao import connect_database
from fastapi import UploadFile

def select_welcome_kit_image(employee_id: int):
    
    connection, cursor  = connect_database()
    
    query = f"""
    SELECT wk.image
    FROM onboarding_me.WelcomeKit wk
    LEFT JOIN Tracking t ON t.welcome_kit_id = wk.id 
    LEFT JOIN Employee e ON t.employee_id = e.id 
    WHERE e.id = {employee_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        
        welcome_kit_image = cursor.fetchone()
        connection.close()
        
        return welcome_kit_image
    

async def insert_welcome_kit(welcome_kit_name: str, welcome_kit_image: UploadFile):    

    connection, cursor  = connect_database()
    
    image_data = await welcome_kit_image.read()
    
    query = f"""
    INSERT INTO onboarding_me.WelcomeKit 
    (name, image)
    VALUES 
    (%s, %s);
    """
    
    try:
       cursor.execute(query, (welcome_kit_name, image_data))
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        connection.commit()
        connection.close()
        return True



def verify_if_welcome_kit_exists(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT wk.id FROM WelcomeKit wk
    LEFT JOIN Tracking t ON t.welcome_kit_id = wk.id 
    LEFT JOIN Employee e ON t.employee_id = e.id 
    WHERE e.id = {employee_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        
        welcome_kit_exists = cursor.fetchone()
        
        if welcome_kit_exists:
            return True
        
    return False