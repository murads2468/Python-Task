
import csv


def generate_gradebook(students_path, scores_path):

    students = {}

    # Read students file
    with open(students_path, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        if reader.fieldnames != ["student_id", "name"]:
            raise ValueError("Invalid students CSV columns")

        for row in reader:

            student_id = row["student_id"].strip()
            name = row["name"].strip()

            if not student_id or not name:
                raise ValueError("Missing student information")

            if student_id in students:
                raise ValueError("Duplicate student ID")

            students[student_id] = {
                "name": name,
                "marks": []
            }

    # Read scores file
    with open(scores_path, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        if reader.fieldnames != ["student_id", "subject", "marks"]:
            raise ValueError("Invalid scores CSV columns")

        seen_subjects = set()

        for row in reader:

            student_id = row["student_id"].strip()
            subject = row["subject"].strip()

            if student_id not in students:
                raise ValueError("Unknown student ID")

            if not subject:
                raise ValueError("Subject cannot be empty")

            key = (student_id, subject)

            if key in seen_subjects:
                raise ValueError("Duplicate student-subject entry")

            seen_subjects.add(key)

            try:
                marks = float(row["marks"])
            except (ValueError, TypeError):
                raise ValueError("Invalid marks")

            if not 0 <= marks <= 100:
                raise ValueError("Marks must be between 0 and 100")

            students[student_id]["marks"].append(marks)

    report = []

    # Calculate average and grade
    for student_id, details in students.items():

        marks = details["marks"]

        average = sum(marks) / len(marks) if marks else 0

        if average >= 85:
            grade = "A"
        elif average >= 70:
            grade = "B"
        elif average >= 55:
            grade = "C"
        elif average >= 40:
            grade = "D"
        else:
            grade = "F"

        report.append({
            "student_id": student_id,
            "name": details["name"],
            "average": round(average, 2),
            "grade": grade
        })

    # Sort by average descending, then student ID ascending
    report.sort(
        key=lambda student: (
            -student["average"],
            student["student_id"]
        )
    )

    # Assign ranks
    for rank, student in enumerate(report, start=1):
        student["rank"] = rank

    # Export report
    with open("report.csv", "w", newline="", encoding="utf-8") as file:

        fieldnames = [
            "student_id", "name", "average", "grade", "rank"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(report)

    return report


# Generate students.csv
with open("students.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow(["student_id", "name"])

    writer.writerow(["101", "Ali"])
    writer.writerow(["102", "Sara"])
    writer.writerow(["103", "Ahmed"])


# Generate scores.csv
with open("scores.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow(["student_id", "subject", "marks"])

    writer.writerow(["101", "Python", 90])
    writer.writerow(["101", "SQL", 80])
    writer.writerow(["101", "Database", 85])

    writer.writerow(["102", "Python", 95])
    writer.writerow(["102", "SQL", 90])

    writer.writerow(["103", "Python", 60])
    writer.writerow(["103", "SQL", 70])


# Generate gradebook
result = generate_gradebook("students.csv", "scores.csv")

for student in result:
    print(student)
