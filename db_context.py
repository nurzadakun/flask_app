import sqlite3


'''Функция предназначена для открытия базы sql и закрытия. 
Если запрос - Select, то она возвращает массив данных
Если запрос Insert, то вносит изменения'''
def db_context(query, commit=False):
    connect = sqlite3.connect('users.db', check_same_thread=False)
    cursor = connect.cursor()

    cursor.execute(query)

    data = []
    
    if commit:
        connect.commit()
    else:
        data = cursor.fetchall()
        
    connect.close()

    return data