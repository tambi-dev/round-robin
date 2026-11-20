def round_robin(processes, quantum):
    # Копируем процессы и добавляем оставшееся время работы.
    pending = []
    for process in processes:
        pending.append({
            "name": process["name"],
            "arrival": process["arrival"],
            "burst": process["burst"],
            "remaining": process["burst"]
        })

    pending.sort(key=lambda process: process["arrival"])
    ready = []
    gantt = []
    completion = {}
    time = 0
    next_process = 0

    while len(completion) < len(processes):
        # Добавляем процессы, которые уже пришли.
        while (
            next_process < len(pending)
            and pending[next_process]["arrival"] <= time
        ):
            ready.append(pending[next_process])
            next_process += 1

        if not ready:
            arrival = pending[next_process]["arrival"]
            gantt.append(("Простой", time, arrival))
            time = arrival
            continue

        current = ready.pop(0)
        duration = min(quantum, current["remaining"])
        start = time
        time += duration
        current["remaining"] -= duration
        gantt.append((current["name"], start, time))

        # Прибытия на границе кванта добавляются перед вытесненным.
        while (
            next_process < len(pending)
            and pending[next_process]["arrival"] <= time
        ):
            ready.append(pending[next_process])
            next_process += 1

        if current["remaining"] > 0:
            ready.append(current)
        else:
            completion[current["name"]] = time

    results = []
    for process in processes:
        name = process["name"]
        finish = completion[name]
        turnaround = finish - process["arrival"]
        waiting = turnaround - process["burst"]
        results.append({
            "name": name,
            "completion": finish,
            "waiting": waiting,
            "turnaround": turnaround
        })

    return gantt, results


if __name__ == "__main__":
    processes = [
        {"name": "P1", "arrival": 0, "burst": 5},
        {"name": "P2", "arrival": 1, "burst": 3},
        {"name": "P3", "arrival": 2, "burst": 1},
        {"name": "P4", "arrival": 3, "burst": 2}
    ]
    quantum = 2
    gantt, results = round_robin(processes, quantum)

    print("Диаграмма Ганта")
    for name, start, end in gantt:
        print(f"{start:>2}–{end:<2}  {name}")

    print("\nПроцесс  Completion  Waiting  Turnaround")
    for row in results:
        print(
            f"{row['name']:<8}"
            f"{row['completion']:<12}"
            f"{row['waiting']:<9}"
            f"{row['turnaround']}"
        )

    average_waiting = sum(row["waiting"] for row in results) / len(results)
    average_turnaround = sum(row["turnaround"] for row in results) / len(results)
    print(f"\nСредний Waiting Time = {average_waiting:.2f}")
    print(f"Средний Turnaround Time = {average_turnaround:.2f}")
