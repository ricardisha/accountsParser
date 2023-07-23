import psycopg2


class dbClass:

    def __init__(self, host, user, password, database):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database    
        )

        self.connection.autocommit = True

    
    def get_couple_info(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT api_key, search_engine_id FROM accounts WHERE status_of_couple='available'")
            return cursor.fetchall()
        
    def set_status_of_couple(self, id_of_couple):
        with self.connection.cursor() as cursor:
            cursor.execute(f"UPDATE accounts SET status_of_couple='unavailable' WHERE id={id_of_couple}")
        
    def close(self):
        self.connection.close()