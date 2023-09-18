from app.dao.dao import connect_database
from app.schemas.address import Address


def select_address(address_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT *
    from Address c 
    WHERE id = {address_id}
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
    
    
def verify_if_address_exists_by_id(address_id: int):
    
    connection, cursor = connect_database()
    
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