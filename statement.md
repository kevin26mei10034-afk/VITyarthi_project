# Project Statement & Specification

## Problem Statement
University students frequently face difficulty managing personal finances due to irregular allowances, lump-sum semester fees, and unexpected daily expenses. Standard commercial budgeting tools are often overly complex, require third-party subscription plans, or lack student-centric features such as hostel bill splitting and lightweight offline execution. 

Without a dedicated, structured tracking mechanism, students risk overspending early in the month, struggling with communal bill balances among roommates, and lacking actionable visibility into their spending distribution across key academic categories.

---

## Scope of the Project
The **Personal Student Expense Tracker** is scoped as a standalone, lightweight command-line interface (CLI) software package built with zero external dependencies.

### In-Scope Capabilities
- Persistent, multi-user storage utilizing embedded SQLite databases.
- Password hashing to protect user data from raw plaintext exposure.
- Record management (Create, Read, Delete) for daily income and spending records.
- Automated calculation of monthly spending against configurable targets.
- Text-based ASCII visual analytics for terminal compatibility.
- Roommate bill splitting algorithm calculating per-person division and total receivable debt.
- Export functionality converting database transaction tables into plain CSV files.

### Out-of-Scope Capabilities
- Graphical User Interfaces (GUI/Web applications).
- Real-time online banking integration or live payment gateway APIs.

---

## Target Users
1. **Undergraduate & Postgraduate Students**: Who need an offline, easy-to-run tool to log daily expenditures (food, mess, transportation, academic supplies).
2. **Hostel & Apartment Residents**: Roommates who regularly pool funds for shared expenses like room rent, electricity, Wi-Fi, and groceries.
3. **Budget-Conscious Individuals**: Students seeking a minimalistic system to avoid exceeding monthly parental or scholarship allowances.

---

## High-Level Features
1. **Authentication & Profile Management (`models.py`)**
   - Hashed user credentials stored in an SQLite table.
   - User profile customization for setting monthly financial spend targets.
2. **Expense Management Subsystem (`models.py`, `main.py`)**
   - Categorized transaction entry (Food, Mess, Academics, Travel, Rent, etc.).
   - Full transaction viewing and ID-based transaction deletion.
3. **Analytics & Budget Alerts Engine (`analytics.py`)**
   - Monthly aggregate spend computation using SQL date functions (`strftime`).
   - Dynamic terminal progress bar visualization using standard block characters (`█`).
   - Automated threshold checking returning "Safe", "80% Warning", or "Over-Budget Alert".
4. **Hostel Bill Splitter Subsystem (`splitter.py`)**
   - Equitable cost sharing formula ($Total \div (Roommates + 1)$).
   - Tracking of individual contributions and aggregate money owed to the user.
5. **Data Portability (`analytics.py`)**
   - File I/O operations exporting database records into readable CSV spreadsheets.