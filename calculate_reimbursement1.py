import sys
import math

# === Input Handling ===
try:
    trip_days = int(float(sys.argv[1]))
    miles = float(sys.argv[2])
    receipts = float(sys.argv[3])
except (IndexError, ValueError):
    print("Error: Please provide valid inputs (trip_days, miles, receipts)")
    sys.exit(1)

mpd = miles / trip_days if trip_days > 0 else 0

# === Base Logic ===
per_diem = trip_days * 100
bonus_for_5_day = 25 if trip_days == 5 else 0
total = per_diem + bonus_for_5_day
print(f"Debug: per_diem = {per_diem:.2f}, bonus_for_5_day = {bonus_for_5_day:.2f}")

# === Trip Type Categorization ===
def trip_type(days):
    if 1 <= days <= 4:
        return "short"
    elif 5 <= days <= 6:
        return "medium"
    elif 7 <= days <= 10:
        return "long"
    else:
        return "extended"
print(f"Debug: trip_type = {trip_type(trip_days)}, mpd = {mpd:.2f}")

# === Travel Bonus Logic ===
if mpd <= 50:
    travel_bonus = 0
elif 51 <= mpd <= 99:
    travel_bonus = 5
elif 100 <= mpd <= 199:
    travel_bonus = 15
else:
    travel_bonus = 30 if trip_type(trip_days) == "short" and mpd > 300 else 50
print(f"Debug: travel_bonus = {travel_bonus:.2f}")

# === Receipt Bonus Logic ===
receipt_bonus = 0
if trip_type(trip_days) == "short":
    if receipts > 1000:
        receipt_bonus = receipts * 0.719  # Special case for high receipts
    else:
        receipt_bonus = min(500, receipts * 0.04)
elif trip_type(trip_days) == "medium":
    receipt_bonus = min(20, receipts * 0.03)
elif trip_type(trip_days) == "long":
    receipt_bonus = min(600, receipts * 0.6)
elif trip_type(trip_days) == "extended":
    receipt_bonus = min(900, receipts * 0.7)
print(f"Debug: receipt_bonus = {receipt_bonus:.2f}")

# === Mileage Calculation ===
if miles <= 100:
    mileage_amt = miles * 0.58
else:
    mileage_amt = 100 * 0.58 + (miles - 100) * 0.30
print(f"Debug: mileage_amt = {mileage_amt:.2f}")

# === Final Total ===
total += mileage_amt + travel_bonus + receipt_bonus
print(f"Debug: total before formatting = {total:.2f}")

# Output the final reimbursement amount
print(f"{total:.2f}")