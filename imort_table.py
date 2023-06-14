import psycopg2
import pandas as pd

# Параметры подключения к базе данных
host = 'your-hostname'
port = 'your-port'
database = 'your-database'
user = 'your-username'
password = 'your-password'

# Путь к файлу с таблицей (например, в формате CSV)
table_file = 'path-to-table-file.csv'

# Чтение таблицы из файла с помощью pandas
table_data = pd.read_csv(table_file)

# Установка соединения с базой данных
connection = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)

try:
    # Создание курсора
    cursor = connection.cursor()

    # Создание временной таблицы для загрузки данных
    create_table_query = '''
    CREATE TEMPORARY TABLE temp_table (
        column1 datatype1,
        column2 datatype2,
        ...
    )
    '''

    cursor.execute(create_table_query)

    # Вставка данных во временную таблицу
    insert_query = '''
    INSERT INTO temp_table (column1, column2, ...)
    VALUES (%s, %s, ...)
    '''

    for _, row in table_data.iterrows():
        data = tuple(row)  # Преобразование строки данных в кортеж
        cursor.execute(insert_query, data)

    # Подтверждение транзакции
    connection.commit()

    print("Таблица успешно загружена в базу данных!")

finally:
    # Закрытие соединения
    cursor.close()
    connection.close()