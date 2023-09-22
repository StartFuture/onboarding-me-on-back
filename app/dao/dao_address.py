from app.dao.dao import connect_database
from app.schemas.address import Address
from app.dao.dao_employee import delete_employees

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
    
    
def select_employees_by_address(address_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT  e.id FROM onboarding_me.Address a 
    LEFT JOIN Employee e ON e.address_id = a.id
    WHERE a.id = {address_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None
    else:
        employees_list = cursor.fetchall()
        connection.close()
        
        ids_list = []
        
        for employee in employees_list:
            ids_list.append(employee['id'])
        
        return ids_list     
    

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
    
    employee_list = select_employees_by_address(address_id)
    
    employee_deleted = delete_employees(employee_list)
    
    if not employee_deleted:
        return False
    
    
    query = f"""
    DELETE FROM onboarding_me.Address
    WHERE id = {address_id}
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


def return_company_addresses(company_id: NotImplemented):
    
    connection, cursor = connect_database()
        
    query = f"""
    SELECT DISTINCT a.id  FROM onboarding_me.Address a 
    LEFT JOIN Employee e ON e.address_id = a.id
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

        addresses_list = cursor.fetchall()
        connection.close()
        
        return addresses_list


def verify_if_address_exists_by_house(company_id: int):
    
    connection, cursor = connect_database()
    
    query = f"""
    SELECT a.num, a.street  FROM Company c
    RIGHT JOIN Employee e ON c.id = e.company_id 
    RIGHT JOIN Address a ON e.address_id = a.id 
    WHERE c.id = {company_id}
    ;
    """
    
    try:
        cursor.execute(query)
        
    except Exception as error:
        connection.close()
        return None    
    
    else:    
        
        addresses_list  = cursor.fetchall()
        connection.close()
        
        return addresses_list