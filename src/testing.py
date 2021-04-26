km = int(input("km: "))
limit = int(input("limit: "))
day = 1

while km <= limit:
    km = km * 0.1 + km
    day += 1
print("This is boy",day ,"days running!")
print(f"This is boy {day} days running!")