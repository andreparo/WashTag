import psycopg2

def get_data(program):
    connection =psycopg2.connect(host = "localhost", database="Washtags", user="postgres", password="pippi2802")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ProgramsWM WHERE numberp = %s", (program,))
    single_program = cursor.fetchone()
    print(single_program)
    cursor.close()
    connection.close()

get_data(1)