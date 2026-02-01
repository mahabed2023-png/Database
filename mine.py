import sqlite3

class ExpsnesMangemant :
  
   def __init__(self, db_name):
       self.co= sqlite3.connect(db_name)
      
       self.cr = self.co.cursor()
       self.cr.execute("""CREATE TABLE IF NOT EXISTS expenses (id integer primary key autoincrement, item text,amount real)""")
       self.co.commit()
    
   def add_expense(self,item_name, price):
      self.cr.execute('''insert into expenses (item , amount) values(?,?)                    
                      ''',(item_name,price))   
      self.co.commit()
      print(f"it`s criet the value {item_name}")    
   def view_all(self): 
       self.cr.execute("select * from expenses")
       
       rows = self.cr.fetchall()
       
       print("---list the costs---")
       for index ,row in enumerate(rows,start=1 ):
           print(f"{index:<5} {row[1]:<15} {row[2]:<10} (ID: {row[0]})")
       print("--------------------")
   
   
   def update_expense(self, expense_id, new_amount):
        self.cr.execute("UPDATE expenses SET amount = ? WHERE id = ?", (new_amount, expense_id))
        self.co.commit()
        print(f"✅ update the price:{expense_id}")

   def delete_expense(self, expense_id):
      
        self.cr.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.co.commit()
        print(f"❌ it done : {expense_id}") 
        
   def get_total_balance(self):
       
        self.cr.execute("SELECT SUM(amount) FROM expenses")
       
        result = self.cr.fetchone()
        
       
        total = result[0]
        
        if total is None:
            total = 0
            
        print(f"\n💰 Total Expenses: {total:.2f}")
        return total     
           
manager = ExpsnesMangemant('APP.db')

while True:
    print("\n1. Add Expense")
    print("2. View All Expenses")
    print("3. Update Expense Amount")
    print("4. Delete Expense")
    print("5. View Total Balance")
    print("6. Exit")
    
    choice = input("Select an option: ")

    if choice == '1':
        item = input("Enter item name: ").strip().capitalize()
        price = float(input("Enter price: "))
        manager.add_expense(item, price)
        
    elif choice == '2':
        manager.view_all()

    elif choice == '3':
        ex_id = int(input("Enter Expense ID to update: "))
        new_p = float(input("Enter new price: "))
        manager.update_expense(ex_id, new_p)

    elif choice == '4':
        ex_id = int(input("Enter Expense ID to delete: "))
        manager.delete_expense(ex_id)
   
    elif choice == '5':
        manager.get_total_balance()
        
    elif choice == '6':
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please try again.")



             
      