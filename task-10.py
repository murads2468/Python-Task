
import csv


def reconcile_inventory(inventory_path, movements_path):

    inventory = {}

    # Read inventory file
    with open(inventory_path, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        if reader.fieldnames != ["sku", "name", "quantity"]:
            raise ValueError("Invalid inventory CSV columns")

        for row in reader:

            sku = row["sku"].strip()
            name = row["name"].strip()

            if not sku or not name or sku in inventory:
                raise ValueError("Invalid or duplicate inventory SKU")

            try:
                quantity = int(row["quantity"])
            except (ValueError, TypeError):
                raise ValueError("Invalid inventory quantity")

            if quantity < 0:
                raise ValueError("Inventory quantity cannot be negative")

            inventory[sku] = {
                "name": name,
                "quantity": quantity
            }

    rejected = []

    # Process movements in order
    with open(movements_path, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        if reader.fieldnames != ["sku", "type", "units"]:
            raise ValueError("Invalid movements CSV columns")

        for line_number, row in enumerate(reader, start=2):

            sku = row["sku"].strip()
            movement_type = row["type"].strip().upper()

            try:
                units = int(row["units"])

                if units <= 0:
                    raise ValueError

            except (ValueError, TypeError):
                rejected.append({
                    "line_number": line_number,
                    "sku": sku,
                    "type": movement_type,
                    "units": row["units"],
                    "reason": "Invalid units"
                })
                continue

            if sku not in inventory:
                reason = "Unknown SKU"

            elif movement_type not in ("IN", "OUT"):
                reason = "Invalid movement type"

            elif movement_type == "OUT" and units > inventory[sku]["quantity"]:
                reason = "Insufficient stock"

            else:
                reason = None

            if reason:

                rejected.append({
                    "line_number": line_number,
                    "sku": sku,
                    "type": movement_type,
                    "units": row["units"],
                    "reason": reason
                })

                continue

            # Apply valid movement
            if movement_type == "IN":
                inventory[sku]["quantity"] += units

            else:
                inventory[sku]["quantity"] -= units

    # Write updated inventory
    with open("updated_inventory.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["sku", "name", "quantity"]
        )

        writer.writeheader()

        for sku, details in inventory.items():

            writer.writerow({
                "sku": sku,
                "name": details["name"],
                "quantity": details["quantity"]
            })

    # Write rejected movements
    with open("rejected_movements.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["line_number", "sku", "type", "units", "reason"]
        )

        writer.writeheader()
        writer.writerows(rejected)

    return inventory, rejected


# Generate inventory.csv
with open("inventory.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow(["sku", "name", "quantity"])

    writer.writerow(["P01", "Laptop", 10])
    writer.writerow(["P02", "Mouse", 20])


# Generate movements.csv
with open("movements.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow(["sku", "type", "units"])

    writer.writerow(["P01", "OUT", 4])
    writer.writerow(["P01", "OUT", 9])
    writer.writerow(["P01", "IN", 2])


# Run reconciliation
result, rejected = reconcile_inventory(
    "inventory.csv",
    "movements.csv"
)

print("Updated Inventory:")

for sku, details in result.items():
    print(sku, details)

print("\nRejected Movements:")
for movement in rejected:
    print(movement)
