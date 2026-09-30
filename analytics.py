import csv
import json
from models import get_db_connection

class AnalyticsManager:
    @staticmethod
    def get_monthly_total(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Sum current month expenses
        cursor.execute('''
            SELECT SUM(amount) as total FROM expenses 
            WHERE user_id = ? AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        ''', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result['total'] if result['total'] else 0.0

    @staticmethod
    def show_category_breakdown(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) as total FROM expenses 
            WHERE user_id = ? GROUP BY category ORDER BY total DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("\nNo expense records found to generate analytics.")
            return

        grand_total = sum(row['total'] for row in rows)
        print("\n" + "="*45)
        print("     CATEGORY EXPENSE ANALYTICS (ASCII)     ")
        print("="*45)
        
        for row in rows:
            cat = row['category']
            amt = row['total']
            percentage = (amt / grand_total) * 100
            bar_length = int(percentage / 5)  # Scale to max 20 bars
            bar = "█" * bar_length
            print(f"{cat[:12]:<12} | {bar:<20} | ₹{amt:<8.2f} ({percentage:.1f}%)")
        
        print("="*45)
        print(f"TOTAL SPENT  : ₹{grand_total:.2f}\n")

    @staticmethod
    def check_budget_status(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT monthly_budget FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        budget = user['monthly_budget'] if user else 0.0
        spent = AnalyticsManager.get_monthly_total(user_id)

        print(f"\n--- Monthly Budget Overview ---")
        print(f"Monthly Budget Target : ₹{budget:.2f}")
        print(f"Current Month Spend   : ₹{spent:.2f}")

        if budget > 0:
            remaining = budget - spent
            if remaining < 0:print(f"⚠️ ALERT: You have exceeded your budget by ₹{abs(remaining):.2f}!")
            elif spent >= 0.8 * budget:print(f"⚠️ WARNING: You have used {((spent/budget)*100):.1f}% of your monthly budget!")
            else:print(f"✅ Safe: You have ₹{remaining:.2f} remaining for this month.")
        else:print("💡 No budget target set. Set one from Profile Settings!")

    @staticmethod
    def export_to_csv(user_id, filename="my_expenses.csv"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, amount, category, description, date FROM expenses WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()

        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Amount', 'Category', 'Description', 'Date'])
            for r in rows:
                writer.writerow([r['id'], r['amount'], r['category'], r['description'], r['date']])
        print(f"\n✅ Data successfully exported to '{filename}'")