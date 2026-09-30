import sys
from models import init_db, UserManager, ExpenseManager
from analytics import AnalyticsManager
from splitter import BillSplitter

def clear_line():
    print("-" * 50)

def main_menu():
    print("""
==================================================
     PERSONAL STUDENT EXPENSE TRACKER CLI
==================================================
1. Register
2. Login
3. Exit
==================================================
""")

def user_dashboard(user):
    while True:
        print(f"""
==================================================
 Welcome, {user['username']}! 
==================================================
1. Add Expense
2. View All Expenses
3. Delete Expense
4. Budget & Analytics (ASCII Chart)
5. Hostel Bill Splitter
6. Set Monthly Budget
7. Export Data to CSV
8. Logout
==================================================
""")
        choice = input("Enter choice (1-8): ").strip()

        if choice == '1':
            try:
                amount = float(input("Enter amount (₹): "))
                print("Categories: [Food, Academics, Rent, Travel, Entertainment, Mess, Others]")
                category = input("Enter category: ").strip().capitalize()
                if not category:
                    category = "Others"
                description = input("Enter description/notes: ").strip()
                ExpenseManager.add_expense(user['id'], amount, category, description)
                print("✅ Expense added successfully!")
                AnalyticsManager.check_budget_status(user['id'])
            except ValueError:
                print("❌ Invalid input! Please enter a numeric amount.")

        elif choice == '2':
            expenses = ExpenseManager.get_user_expenses(user['id'])
            if not expenses:
                print("\nNo expenses logged yet.")
            else:
                print("\n" + "="*60)
                print(f"{'ID':<4} | {'Date':<10} | {'Category':<12} | {'Amount':<8} | {'Notes':<15}")
                print("-" * 60)
                for e in expenses:
                    print(f"{e['id']:<4} | {e['date']:<10} | {e['category'][:12]:<12} | ₹{e['amount']:<7.2f} | {e['description'][:15]:<15}")
                print("="*60)

        elif choice == '3':
            try:
                exp_id = int(input("Enter Expense ID to delete: "))
                if ExpenseManager.delete_expense(exp_id, user['id']):
                    print("✅ Expense deleted successfully.")
                else:
                    print("❌ Expense ID not found.")
            except ValueError:
                print("❌ Invalid input!")

        elif choice == '4':
            AnalyticsManager.show_category_breakdown(user['id'])
            AnalyticsManager.check_budget_status(user['id'])

        elif choice == '5':
            print("\n--- Hostel Bill Splitter ---")
            print("1. Create New Bill Split")
            print("2. View Bill Split History")
            sub_c = input("Choice (1-2): ").strip()
            if sub_c == '1':
                try:
                    title = input("Enter bill description (e.g., Room Rent, Wi-Fi): ").strip()
                    total = float(input("Enter total bill amount (₹): "))
                    count = int(input("Enter number of roommates splitting with you: "))
                    BillSplitter.create_split_bill(user['id'], title, total, count)
                except ValueError:
                    print("❌ Invalid numbers entered.")
            elif sub_c == '2':
                BillSplitter.list_split_bills(user['id'])

        elif choice == '6':
            try:
                b_amt = float(input("Enter your monthly budget target (₹): "))
                UserManager.update_budget(user['id'], b_amt)
                print(f"✅ Monthly budget updated to ₹{b_amt:.2f}")
            except ValueError:
                print("❌ Invalid number.")

        elif choice == '7':
            AnalyticsManager.export_to_csv(user['id'])

        elif choice == '8':
            print(f"Logging out {user['username']}...\n")
            break
        else:
            print("❌ Invalid choice, please try again.")

def main():
    init_db()  # Initialize SQLite database schema
    while True:
        main_menu()
        choice = input("Enter choice (1-3): ").strip()

        if choice == '1':
            print("\n--- Register New User ---")
            uname = input("Enter username: ").strip()
            pwd = input("Enter password: ").strip()
            if uname and pwd:
                success, msg = UserManager.register(uname, pwd)
                print(f"{'✅' if success else '❌'} {msg}")
            else:
                print("❌ Username and password cannot be empty.")

        elif choice == '2':
            print("\n--- Login ---")
            uname = input("Enter username: ").strip()
            pwd = input("Enter password: ").strip()
            user = UserManager.login(uname, pwd)
            if user:
                print(f"\n✅ Login successful!")
                user_dashboard(user)
            else:
                print("❌ Invalid username or password.")

        elif choice == '3':
            print("Exiting application. Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()