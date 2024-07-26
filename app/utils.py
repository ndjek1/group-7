import csv
import os

def load_allowed_users(filename):
    allowed_users = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read header row to find the index of the student number
        student_number_index = header.index('Student_number')
        
        for row in reader:
            allowed_users.append(row[student_number_index])
    
    return allowed_users



def register_attendees(full_name,email,event_name):
        csv_file_path = 'app/docs/event_registrations.csv'

        # Check if the file exists to determine if we need to write headers
        file_exists = os.path.isfile(csv_file_path)

        # Write the form data to the CSV file
        with open(csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ['full_name', 'email', 'event_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()  # write header only if file doesn't exist

            writer.writerow({'full_name': full_name, 'email': email, 'event_name': event_name})


def read_event_registrations():
    csv_file_path = 'app/docs/event_registrations.csv'
    registrations = []

    # Check if the file exists
    if os.path.isfile(csv_file_path):
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                registrations.append(row)

    return registrations