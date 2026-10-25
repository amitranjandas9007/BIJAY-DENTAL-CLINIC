import csv
from pathlib import Path

# Save appointment requests in a CSV file
BASE_DIR = Path(__file__).resolve().parent
APPOINTMENTS_FILE = BASE_DIR / "appointments.csv"


def save_appointment(name, phone, service, date, time):
    file_exists = APPOINTMENTS_FILE.exists()

    with open(APPOINTMENTS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Add column headings when creating the file
        if not file_exists:
            writer.writerow([
                "Customer Name",
                "Phone Number",
                "Requested Service",
                "Preferred Date",
                "Preferred Time",
                "Status"
            ])

        # Save the customer's appointment request
        writer.writerow([
            name,
            phone,
            service,
            date,
            time,
            "Pending Confirmation"
        ])

    print("Appointment request saved successfully!")


if __name__ == "__main__":
    print("BIJAY DENTAL CLINIC - Appointment Request")
    print("----------------------------------------")

    name = input("Enter customer name: ")
    phone = input("Enter customer phone number: ")
    service = input("Enter required treatment: ")
    date = input("Enter preferred appointment date: ")
    time = input("Enter preferred appointment time: ")

    save_appointment(name, phone, service, date, time)

    print("Status: Pending Confirmation")