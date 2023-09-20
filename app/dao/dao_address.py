from app.dao.dao import connect_database
from app.schemas.address import Address


def select_address(employee_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT a.num, a.complement, a.zipcode, a.street, a.district, a.city, a.state  FROM onboarding_me.Address a
    LEFT JOIN Employee e ON e.address_id = a.id
    WHERE e.id = {employee_id}
    ;
    """

    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    
    else:
        address = cursor.fetchone()
        connection.close()
        
        return address
    

def insert_address(address: Address):
    
    connection, cursor = connect_database()
    
    query ="""
    INSERT INTO onboarding_me.Address
    (num, complement, zipcode, street, district, city, state)
    VALUES(%s, %s, %s, %s, %s, %s, %s)
    ;
    """
    
    params = (address.num, address.complement, address.zipcode, address.street, address.district, address.city, address.state)
    
    try:
        cursor.execute(query, params)

    except Exception as error:
        connection.close()
        return False

    else:
        connection.commit()
        connection.close()
        return True
    
    
def update_address(address: Address):
    
    connection, cursor = connect_database()
    
    query ="""
    UPDATE onboarding_me.Address
    SET num = %s, complement = %s, zipcode = %s, street = %s, district = %s, city = %s, state = %s
    WHERE id = %s
    ;
    """
    
    params = (address.num, address.complement, address.zipcode, address.street, address.district, address.city, address.state, address.address_id)
    
    try:
        cursor.execute(query, params)

    except Exception as error:
        connection.close()
        return False

    else:
        connection.commit()
        connection.close()
        return True
    
    
def delete_address(address_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    DELETE FROM onboarding_me.Address
    WHERE id = {address_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except:
        connection.close()
        return False
    else:
        connection.commit()
        connection.close()
        
        return True    
    
    
def verify_if_address_exists(employee_id: int = None, address_id: int = None):
    
    connection, cursor = connect_database()
    
    if employee_id:
        
        query = f"""
        SELECT a.num FROM Address a 
        LEFT JOIN Employee e ON e.address_id = a.id
        WHERE e.id = {employee_id}
        ;
        """
    
    if address_id:
        
        query = f"""
        SELECT id
        FROM onboarding_me.Address
        WHERE id = {address_id}
        ;
        """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False    
    
    else:    
        
        address_exists = cursor.fetchone()
        connection.close()
        
        if address_exists:
            return True
        
    return False


def verify_if_address_exists_by_house(num: str, street: str):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT num
    FROM onboarding_me.Address
    WHERE num = '{num}' AND street = '{street}'
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return False    
    
    else:    
        
        address_exists = cursor.fetchone()
        connection.close()
        
        if address_exists:
            return True
        
    return False