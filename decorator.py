# Database connection decorator
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def db_connection(func):
    """
    Decorator function to establish a database connection before executing the wrapped function
    and close the connection afterward.

    Args:
        func (function): The function to be wrapped.

    Returns:
        function: The wrapper function.
    """

    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('bank.db')
        cursor = connection.cursor()
        try:
            result = func(cursor, *args, **kwargs)
            connection.commit()
            return result
        except Exception as e:
            connection.rollback()
            logger.error(f"Error in {func.__name__}: {e}")
            return f"Error: {e}"
        finally:
            cursor.close()
            connection.close()

    return wrapper
