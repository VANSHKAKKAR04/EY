import json
import random
from faker import Faker

fake = Faker("en_IN")

customers = []

for i in range(1, 501):
    name = fake.name()
    city = fake.city()
    phone = fake.msisdn()[:10]
    salary = random.randint(30000, 150000)
    credit_score = random.randint(550, 900)
    preapproved_limit = random.choice([200000, 300000, 400000, 500000, 600000, 800000])
    existing_loans = random.choice([0, 1, 2, 3])
    age = random.randint(22, 60)

    customers.append({
        "id": i,
        "name": name,
        "age": age,
        "city": city,
        "phone": phone,
        "salary": salary,
        # "credit_score": credit_score,
        "preapproved_limit": preapproved_limit,
        "existing_loans": existing_loans,
    })

with open("data/customers.json", "w") as f:
    json.dump(customers, f, indent=2)

print("✅ customers.json generated with 500 records")
