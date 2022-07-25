import time
from rich.console import Console
import psycopg2
from psycopg2.extras import RealDictCursor
from .core.config import settings

console = Console()

while True:
    try:
        conn = psycopg2.connect(
            database=settings.database,
            user=settings.user,
            port=settings.port,
            password=settings.password,
        )
        cr = conn.cursor()
        console.print(
            "[green bold]SUCCESS[/]:    Connection To Database Established successfuly"
        )
        break
    except psycopg2.OperationalError:
        console.print(
            "[red bold]FAILED[/]:    Connection To Database Failed , Trying Again"
        )
        time.sleep(2)
