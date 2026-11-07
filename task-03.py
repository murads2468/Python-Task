def find_paths(data, target):

    paths = []

    def search(current, current_path):

        if type(current) == type(target) and current == target:
            paths.append(current_path)
            return

        if isinstance(current, dict):

            for key, value in current.items():

                if current_path:
                    new_path = current_path + "." + str(key)
                else:
                    new_path = str(key)

                search(value, new_path)

        elif isinstance(current, list):

            for index, value in enumerate(current):

                new_path = current_path + "[" + str(index) + "]"

                search(value, new_path)

    search(data, "")

    return paths


# Sample data
data = {
    "student": {
        "name": "Ali",
        "marks": [85, 90, {"midterm": 85}]
    },
    "courses": [
        {"SQL": 85},
        {"Python": 90},
        {"Cloud": 85}
    ]
}

# Find all paths
print(find_paths(data, 85))