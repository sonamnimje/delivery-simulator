# FastBox Mystery Delivery System

## Overview

FastBox Mystery Delivery System is a production-style Python logistics simulator. It reads `data.json`, validates the input structure, assigns each package to the nearest available agent using Euclidean distance, simulates delivery movements, and writes a final `report.json` summary.

The implementation is intentionally standard-library only, modular, and suitable for interview-style review or beginner-to-intermediate learning.

## Features

- JSON loading and validation with clear error messages.
- Nearest-agent assignment with deterministic tie-breaking.
- Live agent position updates after every delivery.
- Final report generation with rounded output values.
- CSV export for the best performer.
- Logging to both console and `delivery.log`.
- CLI support with `python main.py data.json`.
- Unit tests using `unittest`.

## Assumptions

- Warehouses and agents are lists of objects with `id` and `location` fields.
- Packages use `warehouse_id` to reference a warehouse.
- Coordinates may be integers or floating-point values, including negatives.
- Distances are calculated with full precision internally and rounded only in the final report.
- If a package is invalid or references a missing warehouse, it is skipped safely and the simulation continues.
- If no package is delivered, `best_agent` is `null` in JSON output.

## Edge Cases Handled

- Empty JSON files.
- Malformed JSON.
- Missing required top-level keys.
- Duplicate warehouse IDs.
- Duplicate agent IDs.
- Empty agents list.
- Empty packages list.
- Invalid or missing warehouse references in packages.
- Invalid package entries that are not objects.
- Equal-distance agents with lexicographic tie-breaking.
- Agent already at the warehouse.
- Destination equal to the warehouse location.
- Warehouses sharing the same coordinates.
- Large package lists processed sequentially.

## Setup Instructions

1. Install Python 3.10 or newer.
2. Open the project folder.
3. No external dependencies are required.

## Execution Steps

Create a virtual environment first:

```powershell
C:\Users\Sonam\AppData\Local\Programs\Python\Python311\python.exe -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run the simulator with the default input file:

```powershell
python main.py
```

Run it with a custom input file:

```powershell
python main.py data.json
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process RemoteSigned` in the current terminal first.

The program writes `report.json`, `top_performer.csv`, and `delivery.log` into the project directory.

## Sample Input

The sample `data.json` uses this shape:

```json
{
  "warehouses": [
    {"id": "W1", "location": [0, 0]}
  ],
  "agents": [
    {"id": "A1", "location": [5, 5]}
  ],
  "packages": [
    {"id": "P1", "warehouse_id": "W1", "destination": [30, 40]}
  ]
}
```

## Sample Output

Console output from the included sample data:

```text
INFO: Package P1 assigned to A1 (warehouse W1 -> destination (30.0, 40.0)).
INFO: Package P2 assigned to A2 (warehouse W2 -> destination (70.0, 90.0)).
INFO: Package P3 assigned to A3 (warehouse W3 -> destination (105.0, 20.0)).
INFO: Package P4 assigned to A1 (warehouse W1 -> destination (10.0, 10.0)).
INFO: Package P5 assigned to A2 (warehouse W2 -> destination (40.0, 80.0)).
FastBox delivery simulation complete.
Packages delivered: 5/5
Best agent: A3
Report saved to: ...\report.json
Top performer CSV: ...\top_performer.csv
FastBox route summary
A1: delivered=2 | distance=121.21
A2: delivered=2 | distance=79.21
A3: delivered=1 | distance=14.14
```

Generated `report.json`:

```json
{
  "A1": {
    "packages_delivered": 2,
    "total_distance": 121.21,
    "efficiency": 60.61
  },
  "A2": {
    "packages_delivered": 2,
    "total_distance": 79.21,
    "efficiency": 39.6
  },
  "A3": {
    "packages_delivered": 1,
    "total_distance": 14.14,
    "efficiency": 14.14
  },
  "best_agent": "A3"
}
```

Generated `top_performer.csv`:

```csv
agent_id,packages_delivered,total_distance,efficiency
A3,1,14.14,14.14
```

## Complexity Analysis

- `get_warehouse_map` and agent-map construction run in $O(W)$ and $O(A)$ time respectively.
- Delivery simulation runs in $O(P \cdot A)$ time because each package scans the current agent positions to find the nearest agent.
- Report generation runs in $O(A)$ time.
- Space usage is $O(W + A + P)$ for the normalized input and runtime state.

## Bonus Features Included

- CSV export for the best performer.
- Logging to `delivery.log`.
- CLI support for alternate input paths.
- Unit tests in `tests/test_main.py`.

## Project Structure

```text
delivery-system/
├── main.py
├── data.json
├── report.json
├── top_performer.csv
├── delivery.log
├── requirements.txt
├── README.md
└── tests/
    └── test_main.py
```