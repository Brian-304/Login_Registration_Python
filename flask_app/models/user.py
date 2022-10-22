from flask_app.config.mysqlconnection import connectToMySQL

class User:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name, email, password, created_at, updated_at) VALUES (%(name)s , %(email)s, %(password)s, NOW() , NOW());"
        return connectToMySQL('login_register').query_db( query, data )
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('login_register').query_db(query,data)
        
        if len(result) < 1:
            return False 
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('login_register').query_db(query,data)
        
        if len(result) < 1:
            return False 
        return cls(result[0])
    
    
    