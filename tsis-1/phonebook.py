import psycopg2
import json
# 🔌 CONNECT TO DB
conn = psycopg2.connect(
   dbname="phonebook_db",
   user="postgres",
   password="123",
   host="localhost",
   port="5432"
)
cur = conn.cursor()
# ➕ ADD CONTACT
def add_contact(name, email, birthday):
   cur.execute(
       "INSERT INTO contacts(name, email, birthday) VALUES (%s, %s, %s)",
       (name, email, birthday)
   )
   conn.commit()
   print("Contact added")
# 🔎 SEARCH
def search_contact(query):
   cur.execute("SELECT * FROM search_contacts(%s)", (query,))
   rows = cur.fetchall()
   print("\nRESULTS:")
   for r in rows:
       print(r)
# 📞 ADD PHONE
def add_phone(name, phone, ptype):
   cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
   conn.commit()
   print("Phone added")
# 🔄 MOVE GROUP
def move_group(name, group):
   cur.execute("CALL move_to_group(%s, %s)", (name, group))
   conn.commit()
   print("Group updated")
# 📤 EXPORT JSON
def export_json():
   cur.execute("""
       SELECT c.name, c.email, c.birthday, g.name
       FROM contacts c
       LEFT JOIN groups g ON c.group_id = g.id
   """)
   data = cur.fetchall()
   result = []
   for row in data:
       result.append({
           "name": row[0],
           "email": row[1],
           "birthday": str(row[2]),
           "group": row[3]
       })
   with open("contacts.json", "w") as f:
       json.dump(result, f, indent=4)
   print("Export done")
# 📥 IMPORT JSON
def import_json():
   with open("contacts.json", "r") as f:
       data = json.load(f)
   for item in data:
       cur.execute("SELECT id FROM contacts WHERE name=%s", (item["name"],))
       exists = cur.fetchone()
       if exists:
           print("Skip:", item["name"])
           continue
       cur.execute(
           "INSERT INTO contacts(name, email, birthday) VALUES (%s, %s, %s)",
           (item["name"], item["email"], item["birthday"])
       )
       conn.commit()
   print("Import done")
# 🎮 MENU
while True:
   print("""
========================
PHONEBOOK TSIS 1
========================
1. Add contact
2. Search contact
3. Add phone
4. Move group
5. Export JSON
6. Import JSON
0. Exit
""")
   choice = input("Choose: ")
   if choice == "1":
       n = input("Name: ")
       e = input("Email: ")
       b = input("Birthday (YYYY-MM-DD): ")
       add_contact(n, e, b)
   elif choice == "2":
       q = input("Search: ")
       search_contact(q)
   elif choice == "3":
       n = input("Contact name: ")
       p = input("Phone: ")
       t = input("Type (home/work/mobile): ")
       add_phone(n, p, t)
   elif choice == "4":
       n = input("Contact name: ")
       g = input("Group: ")
       move_group(n, g)
   elif choice == "5":
       export_json()
   elif choice == "6":
       import_json()
   elif choice == "0":
       break
cur.close()
conn.close()