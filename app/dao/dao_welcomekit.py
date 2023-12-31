from app.dao.dao import connect_database
from app.dao.dao_track_kit import insert_pack

def select_welcome_kit(employee_id: int = None, company_id: int = None):
    
    connection, cursor  = connect_database()
    
    if employee_id:
        
        query = f"""
        SELECT wk.name, wk.image
        FROM WelcomeKit wk
        LEFT JOIN Tracking t ON t.welcome_kit_id = wk.id 
        LEFT JOIN Employee e ON t.employee_id = e.id 
        WHERE e.id = {employee_id}
        ;
        """
        
    if company_id:
        
        query = f"""
        SELECT wk.id, wk.name, wk.image FROM WelcomeKit wk
        LEFT JOIN Tracking t ON t.welcome_kit_id = wk.id 
        LEFT JOIN Employee e ON t.employee_id = e.id 
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
        
        welcome_kits = cursor.fetchall()
        connection.close()
        
        if welcome_kits:
            for item in welcome_kits:
                item['image'] = item['image'].decode('utf-8')
        
        return welcome_kits
    
    
def select_welcome_kit_item(employee_id: int = None, company_id: int = None):
    
    connection, cursor  = connect_database()
    
    if employee_id:
        
        query = f"""
        SELECT wki.name, wki.image  FROM Tracking t
        RIGHT JOIN WelcomeKit wk  ON wk.id = t.welcome_kit_id 
        RIGHT JOIN WelcomeKit_WelcomeKitItem wkwki ON wk.id = wkwki.welcome_kit_id 
        RIGHT JOIN WelcomeKitItem wki ON wki.id = wkwki.item_id
        WHERE t.employee_id = {employee_id}
        ;
        """
    
    if company_id:
        
        query = f"""
        SELECT wki.id, wki.name, wki.image FROM WelcomeKitItem wki 
        LEFT JOIN WelcomeKit_WelcomeKitItem wkwki ON wkwki.item_id = wki.id
        LEFT JOIN WelcomeKit wk ON wk.id = wkwki.welcome_kit_id 
        LEFT JOIN Tracking t ON t.welcome_kit_id = wk.id 
        LEFT JOIN Employee e ON t.employee_id = e.id 
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
        
        welcome_kit_items = cursor.fetchall()
        connection.close()
        
        if welcome_kit_items:
            for item in welcome_kit_items:
                item['image'] = item['image'].decode('utf-8')
        
        return welcome_kit_items
    

def insert_welcome_kit(welcome_kit_name: str = None, welcome_kit_image: str = None, kit_item_name: str = None, kit_item_image: str = None, employee_id: int = None):    

    connection, cursor  = connect_database()
    
    if welcome_kit_name and welcome_kit_image and employee_id:   
            
        query = f"""
        INSERT INTO WelcomeKit 
        (name, image)
        VALUES 
        (%s, %s);
        """
        
        name = welcome_kit_name
        image = welcome_kit_image
        
    if kit_item_name and kit_item_image:
        
        query = f"""
        INSERT INTO WelcomeKitItem
        (name, image)
        VALUES
        (%s, %s)
        ;
        """

        name = kit_item_name
        image = kit_item_image
    
    try:
       cursor.execute(query, (name, image))
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        
        connection.commit()
        
        if name == welcome_kit_name:
            
            query = "SELECT LAST_INSERT_ID() as id_kit FROM WelcomeKit;"
            cursor.execute(query)
            
            id_kit = cursor.fetchone()
            connection.commit()
            connection.close()
            
            link_kit_to_tracking = insert_pack(employee_id=employee_id, welcome_kit_id=id_kit['id_kit'])
            
            if not link_kit_to_tracking:
                return False
        
        
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
   
     
def delete_associate_welcome_kit_items(ids_list: list = None, id_list : list = None):
    
    connection, cursor = connect_database()
     
    if ids_list:
        ids = [item['id'] for item in ids_list]
        
    if id_list:
        ids = id_list
 
 
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
    
    
def delete_all_welcome_kit_items(ids_list: list = None, id_list : list = None):
    
    connection, cursor = connect_database()
     
    if ids_list:
        ids = [item['id'] for item in ids_list]
        
    if id_list:
        ids = id_list
 

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
    
    deleted_associate_items = delete_associate_welcome_kit_items(ids_list=list_items_id)
    
    if not deleted_associate_items:
        return False
    
    deleted_all_items = delete_all_welcome_kit_items(ids_list=list_items_id)
    
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
    
    
def update_welcome_kit(welcome_kit_id: int, welcome_kit_name: str, welcome_kit_image: str):
    
    connection, cursor = connect_database()
    
    query = """
    UPDATE WelcomeKit
    SET 
    name = %s,
    image = %s
    WHERE id = %s
    ;
    """

    params = (welcome_kit_name, welcome_kit_image, welcome_kit_id)
    
    try:
        cursor.execute(query, params)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        
        connection.commit()
        
        list_items_id = select_items_by_welcome_kit_id(welcome_kit_id)
    
        deleted_associate_items = delete_associate_welcome_kit_items(ids_list=list_items_id)
        
        if not deleted_associate_items:
            return False
        
        deleted_all_items = delete_all_welcome_kit_items(ids_list=list_items_id)
        
        if not deleted_all_items:
            return False
        
        return True


def update_welcome_kit_item(kit_id: int, kit_item_name: str, welcome_kit_item_image: str):
    
    connection, cursor = connect_database()
    
    query = """
    UPDATE onboarding_me.WelcomeKitItem
    SET 
    name= %s, 
    image= %s
    WHERE id= %s
    ;
    """
    
    params = (kit_item_name, welcome_kit_item_image, kit_id)

    try:
        cursor.execute(query, params)
        
    except Exception as error:
        connection.close()
        return False
    
    else:
        connection.commit()
        connection.close()
        
        return True

    
def verify_if_welcome_kit_have_this_item(welcome_kit_id: int, item_id: id):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id, welcome_kit_id, item_id
    FROM onboarding_me.WelcomeKit_WelcomeKitItem wkwki
    WHERE wkwki.welcome_kit_id = {welcome_kit_id} AND wkwki.item_id = {item_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        
        welcome_kit_have_this_item = cursor.fetchone()
        
        if welcome_kit_have_this_item:
            return True
        
    return False


def verify_if_welcome_kit_item_exists(kit_item_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT id
    FROM onboarding_me.WelcomeKitItem
    WHERE id = {kit_item_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        
        welcome_kit_item_exists = cursor.fetchone()
        
        if welcome_kit_item_exists:
            return True
        
    return False
    
      
def verify_if_welcome_kit_exists(employee_id: int = None, welcome_kit_id: int = None, company_id: int = None):
    
    connection, cursor = connect_database()
    
    if employee_id:
        
        query = f"""
        SELECT wk.id FROM WelcomeKit wk
        LEFT JOIN Tracking t ON t.welcome_kit_id = wk.id 
        LEFT JOIN Employee e ON t.employee_id = e.id 
        WHERE e.id = {employee_id}
        ;
        """
        
    if company_id:
        
        query = f"""
        SELECT wk.name, wk.image  FROM WelcomeKit wk
        LEFT JOIN Tracking t ON t.welcome_kit_id = wk.id 
        LEFT JOIN Employee e ON t.employee_id = e.id 
        LEFT JOIN Company c ON c.id = e.company_id 
        WHERE c.id = {company_id}
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
