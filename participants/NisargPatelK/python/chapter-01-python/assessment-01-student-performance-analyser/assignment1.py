def handle_input(val, prompt):
    val = -1
    while val < 0 or val > 100:
        try:
            val = float(input(f"Enter Marks for {prompt}: "))
            if val < 0 or val > 100:
                print("Please enter a valid mark between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    return val


def grader(mark):
    if mark >= 100:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 40:
        return "D"
    else:
        return "F"


leaderboard = {}


def add_student_data():
    global name
    global phy, chem, math, bio, hist
    phy = chem = math = bio = hist = 0
    name = input("Enter the student's name: ")
    print("Enter marks for the following subjects (0-100):")
    phy = handle_input(phy, "Physics")
    chem = handle_input(chem, "Chemistry")
    math = handle_input(math, "Mathematics")
    bio = handle_input(bio, "Biology")
    hist = handle_input(hist, "History")

    global total, average
    total = phy + chem + math + bio + hist
    average = total / 5
    leaderboard[name] = total


def output_results():
    print("====================================")
    print("=====Student Performance Report=====")
    print(f"Student Name: {name}")
    print(f"Total Marks: {total}")
    print(f"Average Marks: {average:.2f}")
    print(f"Grade: {grader(average)}")
    print(f"Physics: {phy}")
    print(f"Chemistry: {chem}")
    print(f"Mathematics: {math}")
    print(f"Biology: {bio}")
    print(f"History: {hist}")
    print(f"Grade: {grader(average)}")
    if leaderboard:
        top_student = max(leaderboard, key=leaderboard.get)
        print(f"Highest Performing Student: {top_student} with Total Marks: {leaderboard[top_student]}")
    print("====================================")


def main():
    print("Student Performance Report:")
    while True:
        add_student_data()
        output_results()


if __name__ == "__main__":
    main()
