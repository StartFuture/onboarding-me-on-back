from app.dao.dao import connect_database
from fastapi import UploadFile


def select_welcome_kit_image(employee_id: int):
    
    connection, cursor  = connect_database()
    
    query = f"""
    SELECT wk.image
    FROM WelcomeKit wk
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
    
    
def select_welcome_kit_item_image(welcome_kit_id: int, item_id: int):
    
    connection, cursor  = connect_database()
    
    query = f"""
    SELECT wki.name, wki.image 
    FROM WelcomeKit_WelcomeKitItem wkwki
    RIGHT JOIN WelcomeKitItem wki ON wki.id = wkwki.item_id 
    WHERE wkwki.welcome_kit_id = {welcome_kit_id} AND wkwki.item_id = {item_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        
        welcome_kit_item_image = cursor.fetchone()
        connection.close()
        
        return welcome_kit_item_image
    

async def insert_welcome_kit(welcome_kit_name: str = None, welcome_kit_image: UploadFile = None, kit_item_name: str = None, kit_item_image: UploadFile = None):    

    connection, cursor  = connect_database()
    
    if welcome_kit_name and welcome_kit_image:   
            
        query = f"""
        INSERT INTO WelcomeKit 
        (name, image)
        VALUES 
        (%s, %s);
        """
        image_data = await welcome_kit_image.read()
        name = welcome_kit_name
        
    if kit_item_name and kit_item_image:
        
        query = f"""
        INSERT INTO WelcomeKitItem
        (name, image)
        VALUES
        (%s, %s)
        ;
        """

        image_data = await kit_item_image.read()
        name = kit_item_name
    
    
    try:
       cursor.execute(query, (name, image_data))
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        
        connection.commit()
        
        if name == kit_item_name:
            
            query = "SELECT LAST_INSERT_ID() as id_item FROM WelcomeKitItem wki;"
    
            cursor.execute(query)
            id_item = cursor.fetchone()
            connection.commit()

            connection.close()

            return id_item
        
        
        connection.close()
        return True
    
    
def associate_item_with_kit(welcome_kit_id: int, item_id: int):
    
    connection, cursor  = connect_database()
    
    query = f"""
    INSERT INTO onboarding_me.WelcomeKit_WelcomeKitItem
    (welcome_kit_id, item_id)
    VALUES
    ({welcome_kit_id}, {item_id})
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
    
    
def select_items_by_welcome_kit_id(welcome_kit_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT wki.id
    FROM onboarding_me.WelcomeKitItem wki
    LEFT JOIN WelcomeKit_WelcomeKitItem wkwki ON wkwki.item_id = wki.id 
    LEFT JOIN WelcomeKit wk ON wkwki.welcome_kit_id = wk.id 
    WHERE wk.id = {welcome_kit_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        
        list_items_id = cursor.fetchall()
        
        return list_items_id
   
     
def delete_associate_welcome_kit_items(ids_list: list):
    
    connection, cursor = connect_database()
     
    ids = [item['id'] for item in ids_list]
 
    placeholder = ','.join(['%s'] * len(ids))
    
    query = f"""
    DELETE FROM WelcomeKit_WelcomeKitItem
    WHERE item_id IN ({placeholder});
    ;
    """
    
    try:
        cursor.execute(query, (ids))
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        connection.commit()
        connection.close()
    
        return True
    
    
def delete_all_welcome_kit_items(ids_list: list):
    
    connection, cursor = connect_database()
     
    ids = [item['id'] for item in ids_list]
 
    placeholder = ','.join(['%s'] * len(ids))
    
    query = f"""
    DELETE FROM WelcomeKitItem
    WHERE id IN ({placeholder});
    ;
    """
    
    try:
        cursor.execute(query, (ids))
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        connection.commit()
        connection.close()
    
        return True
    
    
def delete_tracking_welcome_kit(welcome_kit_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    DELETE FROM Tracking t
    WHERE t.welcome_kit_id = {welcome_kit_id}
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
    
    
def delete_welcome_kit(welcome_kit_id: int):
    
    connection, cursor = connect_database()
    
    list_items_id = select_items_by_welcome_kit_id(welcome_kit_id)
    
    deleted_associate_items = delete_associate_welcome_kit_items(list_items_id)
    
    if not deleted_associate_items:
        return False
    
    deleted_all_items = delete_all_welcome_kit_items(list_items_id)
    
    if not deleted_all_items:
        return False
    
    deleted_tracking = delete_tracking_welcome_kit(welcome_kit_id)
    
    if not deleted_tracking:
        return False
    
    query = f"""
    DELETE FROM WelcomeKit 
    WHERE id = {welcome_kit_id}
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
    
    
def verify_if_welcome_kit_exists(employee_id: int = None, welcome_kit_id: int = None):
    
    connection, cursor = connect_database()
    
    if employee_id:
        
        query = f"""
        SELECT wk.id FROM WelcomeKit wk
        LEFT JOIN Tracking t ON t.welcome_kit_id = wk.id 
        LEFT JOIN Employee e ON t.employee_id = e.id 
        WHERE e.id = {employee_id}
        ;
        """
    
    if welcome_kit_id:
        
        query = f"""
        SELECT id
        FROM WelcomeKit
        WHERE id = {welcome_kit_id}
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
