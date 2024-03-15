from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DB = os.getenv("DB_DATABASE")

LLM_LOGGER_NAME = "code_snippet.llm_logger"


class Database:

    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.docker_host = HOST
            self.docker_port = PORT
            self.postgres_user = USER
            self.postgres_password = PASSWORD
            self.postgres_db = DB
            self.db_url = f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.docker_host}:{self.docker_port}/{self.postgres_db}"
            self.engine = create_engine(self.db_url)
            self.connection = self.engine.connect()
        except Exception as e:
            print(e)
            raise e

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        try:
            result = self.connection.execute(text(query))
            self.connection.commit()
            return result
        except Exception as e:
            print(e)
            raise e

    def insert_llm_logger(self, query, response, user_id):
        try:
            query = query.replace("'", "''")
            response = response.replace("'", "''")

            start_index = response.find("```")
            end_index = response.find("```", start_index + 1)
            if start_index != -1 and end_index != -1 and start_index != end_index:
                snippets = response[start_index + 3:end_index]
            else:
                snippets = None

            insert_query = f"""
                        INSERT INTO {LLM_LOGGER_NAME} 
                        (query, response, user_id, snippets) 
                        VALUES 
                        ('{query}', '{response}', '{user_id}', {'NULL' if snippets is None else f"'{snippets}'"})
                        RETURNING response_id
                    """
            result = self.execute_query(insert_query)
            result = result.fetchone()[0]
            return result
        except Exception as e:
            print(e)
            raise e

    def get_chat_history(self, user_id):
        try:
            chat_history = []

            select_query = f"""
                        SELECT query, response 
                        FROM {LLM_LOGGER_NAME}
                        WHERE user_id = '{user_id}'
                        ORDER BY response_id
                    """
            result = self.execute_query(select_query)
            rows = result.fetchall()

            for row in rows:
                query_content = row[0]
                response_content = row[1]

                # Create user query object
                chat_history.append({"role": "user", "content": query_content})

                # Create assistant response object
                chat_history.append({
                    "role": "assistant",
                    "content": response_content
                })

            return chat_history
        except Exception as e:
            print(e)
            raise e

    def get_snippets(self, user_id):
        try:
            select_query = f"""
                SELECT response_id, snippets 
                FROM {LLM_LOGGER_NAME}
                WHERE user_id = '{user_id}'
                ORDER BY response_id
            """
            result = self.execute_query(select_query)
            rows = result.mappings().all()
            snippets = []
            for row in rows:
                response_id = row["response_id"]
                snippet = row["snippets"]
                if snippet:
                    snippets.append({
                        "response_id": response_id,
                        "snippets": snippet
                    })

            return snippets
        except Exception as e:
            print(e)
            raise e

    def delete_snippet(self, response_id):
        try:
            delete_query = f"""
                DELETE 
                FROM {LLM_LOGGER_NAME}
                WHERE response_id = '{response_id}'
            """
            self.execute_query(delete_query)
            return "Deleted"
        except Exception as e:
            print(e)
            raise e

    def edit_snippet(self, response_id, snippet):
        try:
            edit_query = f"""
                UPDATE {LLM_LOGGER_NAME}
                SET snippets = '{snippet}'
                WHERE response_id = '{response_id}'
            """
            self.execute_query(edit_query)
            return "Edited"
        except Exception as e:
            print(e)
            raise e
