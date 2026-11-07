
def plan_execution(tasks, dependencies):

    if len(tasks) != len(set(tasks)):
        raise ValueError("Duplicate task names are not allowed")

    if not all(isinstance(task, str) and task.strip() for task in tasks):
        raise ValueError("Invalid task name")

    graph = {task: [] for task in tasks}
    in_degree = {task: 0 for task in tasks}

    # Build dependency graph
    for first, second in dependencies:

        if first not in graph or second not in graph:
            raise ValueError("Unknown task name found")

        if second in graph[first]:
            continue

        graph[first].append(second)
        in_degree[second] += 1

    # Find tasks with no prerequisites
    available = sorted(
        task for task in tasks if in_degree[task] == 0
    )

    execution_order = []

    # Execute tasks in alphabetical order
    while available:

        current_task = available.pop(0)
        execution_order.append(current_task)

        for next_task in graph[current_task]:

            in_degree[next_task] -= 1

            if in_degree[next_task] == 0:
                available.append(next_task)

        available.sort()

    # Detect cycle
    if len(execution_order) != len(tasks):
        raise ValueError("Cycle detected in task dependencies")

    return execution_order


# Sample data
tasks = ["database", "frontend", "backend", "testing", "deployment"]

dependencies = [
    ("database", "backend"),
    ("backend", "frontend"),
    ("frontend", "testing"),
    ("testing", "deployment")
]

# Display execution order
print(plan_execution(tasks, dependencies))
