import gzip
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "logdive.db"
DB_PATH.unlink()
LOGS_DIR = Path("./logs")

con = sqlite3.connect(DB_PATH)
con.execute('begin')
con.execute("create table logs(filename, line)")

gzipped_logs = LOGS_DIR.glob("*.gz")

gzipped_logs.sort(key=lambda x: x.name)

outputs = []

for gzipped_log in gzipped_logs:
    log_name = gzipped_log.name

    print(f"Processing {log_name}")

    with gzip.open(gzipped_log, 'rt') as f:
        lines = f.readlines()
        for line in lines:
            outputs.append((
                log_name,
                line
            ))

print("Done processing logs, inserting into database")

con.executemany("insert into logs(filename, line) values (?,?)", outputs)
con.execute("end")
con.commit()

print(f"Done! saved to {DB_PATH}")
