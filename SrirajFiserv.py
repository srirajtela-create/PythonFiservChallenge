//FiservChallenge Questions Codes

FOR QUESTION-1 BELOW IS THE CODE
# Custom Exception class
class ValidationException(Exception):
    pass

def validate_file(filename):
    try:
        with open(filename, "r") as file:
            next(file)  # skip header line
            for line in file:
                parts = line.strip().split(",")
                if len(parts) < 2:
                    continue

                mileage = parts[1].strip()  # second column is mileage
                # check if mileage is a valid integer
                if not mileage.isdigit():
                    raise ValidationException(f"Invalid mileage:  {mileage}")
    except FileNotFoundError:
        raise ValidationException(f"File not found: {filename}")

def ex1():
    try:
        validate_file("input.txt")
    except ValidationException as ve:
        print(ve)

# Run
ex1()

//FOR QUESTION-2 BELOW IS THE CODE

import pandas as pd

def find_total_visits():
    # Read the three weekly CSV files
    week1 = pd.read_csv("week-1.csv")
    week2 = pd.read_csv("week-2.csv")
    week3 = pd.read_csv("week-3.csv")

    # Calculate total visits for each week (exclude 'Name' column)
    total_week1 = week1.iloc[:, 1:].sum().sum()
    total_week2 = week2.iloc[:, 1:].sum().sum()
    total_week3 = week3.iloc[:, 1:].sum().sum()

    # Return total visits across all weeks
    return int(total_week1 + total_week2 + total_week3)

def ex2():
    total = find_total_visits()
    print(f"Total visits: {total}.")

# Run the function
if __name__ == "__main__":
    ex2()

//FOR QUESTION-3 BELOW IS THE CODE

import re

def count_words(filename):
    # Read the file contents
    with open(filename, 'r') as file:
        text = file.read()

    # Extract words (ignore punctuation)
    words = re.findall(r'\b\w+\b', text)

    # Separate small and large words
    small_words = set()
    large_words = set()

    for word in words:
        if len(word) < 3:
            small_words.add(word)
        else:
            large_words.add(word)

    # Write small words to a file
    with open("small-words.txt", 'w') as sw:
        for word in sorted(small_words):
            sw.write(word + "\n")

    # Write large words to a file
    with open("large-words.txt", 'w') as lw:
        for word in sorted(large_words):
            lw.write(word + "\n")

    # Return total number of unique words
    return len(small_words.union(large_words))

def ex3():
    total_words = count_words("words.txt")
    print(f"Total words: {total_words}.")

# Run the example
if __name__ == "__main__":
    ex3()
//FOR THE QUESTION-4 BELOW CODE
import boto3

def calculate():
    log = []  # to store calculations

    while True:
        num1 = input("Enter first number (or 'q' to quit): ").strip()
        if num1.lower() == 'q':
            break
        num2 = input("Enter second number: ").strip()

        # Validate numeric input
        try:
            n1 = float(num1)
            n2 = float(num2)
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue

        result = n1 + n2
        print(f"{n1} + {n2} = {result}")
        log.append(f"{n1} + {n2} = {result}")

    # Write log to file (append your student ID)
    student_id = "123456"  # <-- replace with your actual student ID
    filename = f"calculator-log-{student_id}.txt"

    with open(filename, "w") as f:
        f.write("\n".join(log))

    # Upload to S3
    try:
        s3 = boto3.client('s3')
        bucket_name = "your-s3-bucket-name"  # <-- replace with your S3 bucket
        s3.upload_file(filename, bucket_name, filename)
        print("*** Uploaded to S3 ***")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

def ex4():
    calculate()

# Run the example
if __name__ == "__main__":
    ex4()

//FOR THE QUESTION-5 BELOW CODE

from pprint import pprint

def build_car_list():
    # Read car ID and model mapping
    car_models = {}
    with open("car-ids.txt", "r") as f:
        next(f) # skip header line
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 2:
                try:
                    car_id = int(parts[0].strip())
                    model = parts[1].strip()
                    car_models[car_id] = model
                except ValueError:
                    print(f"Skipping invalid car ID line: {line.strip()}")


    # Read mileage data
    cars = []
    with open("input.txt", "r") as f:
        next(f) # skip header line
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 2:
                try:
                    car_id = int(parts[0].strip())
                    miles = int(parts[1].strip())
                    if car_id in car_models:
                        cars.append({"id": car_id, "miles": miles, "model": car_models[car_id]})
                except ValueError:
                    print(f"Skipping invalid mileage line: {line.strip()}")


    # Detect outlier mileage values (e.g., > 100000 or < 1000)
    cleaned_cars = [car for car in cars if 1000 <= car["miles"] <= 100000]

    return cleaned_cars

def ex5():
    car_list = build_car_list()
    pprint(car_list)

# Run the example
if __name__ == "__main__":
    ex5()

!pip install boto3

"""After running the cell above to install `boto3`, you can run the original code cell again."""
