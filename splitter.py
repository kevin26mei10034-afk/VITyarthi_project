from datetime import datetime
from models import get_db_connection


class BillSplitter:

    @staticmethod
    def create_split_bill(user_id, title, total_amount, roommates_count):

        # Roommates cannot be zero or less
        if roommates_count <= 0:
            print("Roommates count must be greater than 0.")
            return

        # Total people = you + roommates
        totalPeople = roommates_count + 1

        # Calculate each person's share
        perPerson = total_amount / totalPeople

        # Get today's date
        today = datetime.now().strftime("%Y-%m-%d")

        # Save bill split to database
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO split_bills
        (user_id, title, total_amount, per_person, roommates_count, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                user_id,
                title,
                total_amount,
                perPerson,
                roommates_count,
                today
            )
        )

        conn.commit()
        conn.close()

        # Calculate total amount owed to you
        owedToMe = perPerson * roommates_count

        # Display result
        print("")
        print("=" * 40)
        print("          BILL SPLIT CREATED          ")
        print("=" * 40)
        print("Bill Title          : " + str(title))
        print("Total Amount        : ₹%.2f" % total_amount)
        print(
            "People Sharing      : "
            + str(totalPeople)
            + " (You + "
            + str(roommates_count)
            + " roommates)"
        )
        print("Your Share          : ₹%.2f" % perPerson)
        print("Owed to You (Total) : ₹%.2f" % owedToMe)
        print("Owed Per Roommate   : ₹%.2f" % perPerson)
        print("=" * 40)
        print("")

    @staticmethod
    def list_split_bills(user_id):

        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get all bill splits for this user
        cursor.execute(
            """
            SELECT *
            FROM split_bills
            WHERE user_id = ?
            ORDER BY date DESC
            """,
            (user_id,)
        )

        bills = cursor.fetchall()

        # Close database connection
        conn.close()

        # Nothing in the table
        if len(bills) == 0:
            print("")
            print("No bill splits found.")
            return

        # Display bill split history
        print("")
        print("=" * 80)
        print("                    BILL SPLIT HISTORY")
        print("=" * 80)

        for bill in bills:
            print("")
            print("Bill ID             : " + str(bill[0]))
            print("Bill Title          : " + str(bill[2]))
            print("Total Amount        : ₹%.2f" % bill[3])
            print("Per Person          : ₹%.2f" % bill[4])
            print("Roommates           : " + str(bill[5]))
            print("Date                : " + str(bill[6]))

            totalPeople = bill[5] + 1
            owedToMe = bill[4] * bill[5]

            print("People Sharing      : " + str(totalPeople))
            print("Owed to You         : ₹%.2f" % owedToMe)

            print("-" * 80)

        print("=" * 80)
        print("")
