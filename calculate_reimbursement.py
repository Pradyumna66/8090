import sys
import math

# === Input Handling ===
trip_days = int(float(sys.argv[1]))
miles = float(sys.argv[2])
receipts = float(sys.argv[3])
mpd = miles / trip_days if trip_days > 0 else 0  # miles per day

# === Base Logic ===
per_diem = trip_days * 100
bonus_for_5_day = 25 if trip_days == 5 else 0
total = per_diem + bonus_for_5_day

# === Helper Functions ===
def gaussian_taper(x, peak, std_dev, max_bonus):
    return max_bonus * math.exp(-((x - peak) ** 2) / (2 * std_dev ** 2))

def trip_type(days):
    if 1 <= days <= 4:
        return "short"
    elif 5 <= days <= 6:
        return "medium"
    elif 7 <= days <= 10:
        return "long"
    else:
        return "extended"

trip = trip_type(trip_days)

# === Travel Bonus Logic (Refined) ===
travel_bonus = 0

if mpd <= 25:
    travel_bonus = -50
elif 26 <= mpd <= 99:
    travel_bonus = 50
elif 100 <= mpd <= 199:
    travel_bonus = 100
elif mpd >= 200:
    # Enhanced high-mileage bonus with better curve fitting
    if mpd <= 300:
        travel_bonus = 100 + (mpd - 200) * 2  # Linear increase
    elif mpd <= 500:
        travel_bonus = 300 + (mpd - 300) * 1.5  # Slower increase
    elif mpd <= 800:
        travel_bonus = 600 + (mpd - 500) * 1    # Even slower
    else:
        travel_bonus = 900 + (mpd - 800) * 0.5  # Diminishing returns
    
    # Cap at reasonable maximum
    travel_bonus = min(travel_bonus, 1200)

# === Receipt Bonus Logic (Completely Rewritten) ===
receipt_bonus = 0

# Universal penalty for very low receipts
if receipts < 50:
    receipt_bonus = -50
else:
    if trip == "short":  # 1-4 days
        if 50 <= receipts < 100:
            receipt_bonus = 75
        elif 100 <= receipts < 300:
            receipt_bonus = 100
        elif 300 <= receipts < 600:
            receipt_bonus = 100 + (receipts - 300) * 0.5
        elif 600 <= receipts < 1000:
            receipt_bonus = 250 + (receipts - 600) * 0.8
        elif receipts >= 1000:
            # High receipt bonus with Gaussian peak
            receipt_bonus = max(570, gaussian_taper(receipts, peak=1400, std_dev=400, max_bonus=800))
    
    elif trip == "medium":  # 5-6 days
        if 50 <= receipts < 100:
            receipt_bonus = 60
        elif 100 <= receipts < 120:
            receipt_bonus = 100
        elif 120 <= receipts < 400:
            receipt_bonus = 100 - (receipts - 120) * 0.15  # Gentle decline
        elif 400 <= receipts < 800:
            receipt_bonus = 58 + (receipts - 400) * 0.3
        elif receipts >= 800:
            # Medium trip high receipt bonus
            receipt_bonus = max(178, gaussian_taper(receipts, peak=1200, std_dev=350, max_bonus=650))
    
    elif trip == "long":  # 7-10 days
        if 50 <= receipts < 90:
            receipt_bonus = 100
        elif 90 <= receipts < 100:
            receipt_bonus = gaussian_taper(receipts, peak=90, std_dev=5, max_bonus=80)
        elif 100 <= receipts < 200:
            receipt_bonus = 70 - (receipts - 100) * 0.2
        elif 200 <= receipts < 600:
            receipt_bonus = 50 + (receipts - 200) * 0.25
        elif receipts >= 600:
            # Long trip high receipt bonus
            receipt_bonus = max(150, gaussian_taper(receipts, peak=1500, std_dev=500, max_bonus=700))
    
    elif trip == "extended":  # 11+ days
        if 50 <= receipts < 200:
            receipt_bonus = 100
        elif 200 <= receipts < 500:
            receipt_bonus = 100 + (receipts - 200) * 0.2
        elif 500 <= receipts < 1000:
            receipt_bonus = 160 + (receipts - 500) * 0.4
        elif receipts >= 1000:
            # Extended trip high receipt bonus
            receipt_bonus = max(360, gaussian_taper(receipts, peak=1800, std_dev=600, max_bonus=900))

# === Mileage Calculation ===
if miles <= 100:
    mileage_amt = miles * 0.58
else:
    mileage_amt = 100 * 0.58 + (miles - 100) * 0.30

# === Special Bonuses ===
super_bonus = 0

# Elite single-day trips with high mileage and receipts
if trip_days == 1 and mpd > 100 and receipts > 1000:
    super_bonus += 250

# High-mileage long trips bonus
if trip_days >= 7 and miles > 1000:
    super_bonus += min(100, (miles - 1000) * 0.1)

# Medium trips with very high receipts
if trip == "medium" and receipts > 1000:
    super_bonus += min(150, (receipts - 1000) * 0.1)

# Extended trips with high mileage
if trip_days >= 11 and miles > 800:
    super_bonus += min(200, (miles - 800) * 0.15)

# Very high MPD bonus (above 600)
if mpd > 600:
    super_bonus += min(300, (mpd - 600) * 0.3)

# === Special Adjustments ===
# Adjustment for very short trips with high receipts but low miles
if trip_days <= 2 and receipts > 1500 and miles < 200:
    receipt_bonus *= 0.7  # Reduce receipt bonus

# Adjustment for very long trips with low receipts
if trip_days >= 10 and receipts < 300:
    travel_bonus += 50  # Small compensation

# === Final Total ===
total += mileage_amt + travel_bonus + receipt_bonus + super_bonus

# Ensure minimum reimbursement
total = max(total, 50)

# Output the final reimbursement amount
print(f"{total:.2f}")