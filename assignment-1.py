# This program analyzes student marks using Python and NumPy.
# It assigns grades, calculates statistics (mean, median, max, min, and standard deviation),
# and identifies students who scored above average and those with an A grade.
# This program stores student marks and assigns grades based on their scores.
# It uses NumPy to calculate statistics and analyze student performance efficiently.
import numpy as np

# Store student marks
marks = [72, 85, 90, 45, 63, 78, 91, 56, 88, 67]

# Function to assign grades
def grade(score):
    if score >= 85:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "F"

print("Student Grades")
for i, score in enumerate(marks, start=1):
    print(f"Student {i}: {score} -> {grade(score)}")

marks_array = np.array(marks)

print("\nMean:", np.mean(marks_array))
print("Median:", np.median(marks_array))
print("Maximum:", np.max(marks_array))
print("Minimum:", np.min(marks_array))
print("Standard Deviation:", np.std(marks_array))

average = np.mean(marks_array)
print("\nStudents Above Average:", np.sum(marks_array > average))

print("\nA Grade Students:")
print(marks_array[marks_array >= 85])

# Bonus
new_scores = [80, 95, 60, 74, 50]
marks.extend(new_scores)

marks_array = np.array(marks)

grades = [grade(score) for score in marks]

count = {}
for g in grades:
    count[g] = count.get(g, 0) + 1

print("\nGrade Counts:", count)
print("Most Common Grade:", max(count, key=count.get))
