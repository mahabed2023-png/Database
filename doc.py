import sqlite3

# ----------------- Database Logic -----------------

db = sqlite3.connect("hos.db")

cr = db.cursor()

cr.execute("""
           CREATE TABLE IF NOT EXISTS doctors( 
           id INTEGER PRIMARY KEY,
           name TEXT NOT NULL,
           specialization TEXT NOT NULL,
           phone TEXT NOT NULL
           )""")


# cr.execute("""
#            insert into doctors (name, specialization, phone)
#            values
#            ('Dr. John Smith', 'Cardiology', '555-1234'),
#            ('Dr. Emily Davis', 'Neurology', '555-5678'),
#            ('Dr. Michael Brown', 'Pediatrics', '555-8765')          
#            """)


cr.execute("delete from doctors where id=4")

# cr.execute("update doctors set phone='555-9999' where id=2")

cr.execute("select * from doctors")
results = cr.fetchall()

for row in results:
      print(f"{row[0]}-",end=" ")
      print(f"name=> {row[1]},",end=" ")
      print(f"specialization=> {row[2]},",end=" ")
      print(f"phone=> {row[3]}")




db.commit()
db.close()