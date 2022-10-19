from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from models.message import Message


class MessageDb(object):
    def __init__(self, host, port, auth) -> None:
        self.__auth = auth
        auth_provider = PlainTextAuthProvider(username=self.__auth["username"],
                                              password=self.__auth["password"])
        cluster = Cluster([host], port=port,
                          auth_provider=auth_provider)

        # To establish connection and begin executing queries, need a session
        session = cluster.connect()
        self.__cluster = cluster
        self.__session = session

    def initialize_db(self):
        # Create a Keyspace and Message table for the project
        try:
            self.__session.execute("""
            CREATE KEYSPACE IF NOT EXISTS insta 
            WITH REPLICATION = 
            { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }""")
            self.__session.set_keyspace('insta')
            self.__create_message_table()
        except Exception as error:
            print(error)

    def __create_message_table(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS machine_message"
        create_table_query = create_table_query + \
            "(id int, message_type text, start_time timestamp, status_code int, machine_id int, \
                PRIMARY KEY ((id, machine_id), start_time)) WITH CLUSTERING ORDER BY (start_time DESC)"
        try:
            self.__session.execute(create_table_query)
        except Exception as error:
            print(error)

    def insert_message(self, message: Message):
        # Assign the INSERT statements into the `query` variables with values extracted above
        query = "INSERT INTO machine_message (id, message_type, start_time, status_code, machine_id)"
        query = query + " VALUES (%s, %s, %s, %s, %s)"
        # Assign which column element should be assigned for each column in the INSERT statement.
        try:
            self.__session.execute(
                query, (message.id, message.message_type, message.start_time, message.status_code, message.machine_id))
        except Exception as error:
            print(error)

    def query_message(self):
        query = "SELECT id , message_type , start_time, status_code, machine_id FROM machine_message"
        try:
            rows = self.__session.execute(query)
        except Exception as error:
            print(error)

        sorted_rows = list(rows)
        sorted_rows.sort(key=lambda x: x.start_time, reverse=True)
        message = [{"id": row.id, "type": row.message_type, "time": row.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                    "status": row.status_code, "machineId": row.machine_id} for row in sorted_rows]
        return message

    def shutdown_db(self):
        query = "drop table machine_message"
        try:
            self.__session.execute(query)
        except Exception as error:
            print(error)
        self.__session.shutdown()
        self.__cluster.shutdown()
