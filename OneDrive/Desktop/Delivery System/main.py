"""FastBox Mystery Delivery System.

Production-quality delivery simulator for the FastBox assignment.
The program reads JSON input, validates the structure, assigns each package to
the nearest agent by current agent position, simulates the route, and writes a
report plus an optional top-performer CSV file.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


Coordinate = Tuple[float, float]
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_FILE = BASE_DIR / "data.json"
DEFAULT_REPORT_FILE = BASE_DIR / "report.json"
DEFAULT_CSV_FILE = BASE_DIR / "top_performer.csv"
DEFAULT_LOG_FILE = BASE_DIR / "delivery.log"

LOGGER = logging.getLogger("fastbox")


@dataclass
class AgentState:
    """Mutable runtime state for a delivery agent."""

    agent_id: str
    position: Coordinate
    packages_delivered: int = 0
    total_distance: float = 0.0


def _configure_logging(log_path: Path = DEFAULT_LOG_FILE) -> logging.Logger:
    """Configure console and file logging without duplicating handlers."""

    logger = logging.getLogger("fastbox")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass

    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


def load_data(filepath: str | Path) -> Dict[str, Any]:
    """Load JSON data from disk and ensure it is a JSON object.

    Args:
        filepath: Path to the input JSON file.

    Returns:
        Parsed JSON document.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty, malformed, or the top-level JSON value
            is not an object.
    """

    path = Path(filepath)
    raw_text = path.read_text(encoding="utf-8")
    if not raw_text.strip():
        raise ValueError("Input JSON file is empty.")

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON in {path}: {exc.msg}") from exc

    if not isinstance(data, dict):
        raise ValueError("The top-level JSON value must be an object.")

    return data


def _normalize_coordinate(value: Any, label: str) -> Coordinate:
    """Convert a coordinate-like value into a numeric two-item tuple."""

    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"{label} must be a two-item coordinate list.")

    try:
        return float(value[0]), float(value[1])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must contain numeric values.") from exc


def calculate_distance(point1: Sequence[float], point2: Sequence[float]) -> float:
    """Calculate the Euclidean distance between two points."""

    x1, y1 = float(point1[0]), float(point1[1])
    x2, y2 = float(point2[0]), float(point2[1])
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_warehouse_map(warehouses: Any) -> Dict[str, Coordinate]:
    """Convert warehouse records into an O(1) lookup map.

    Raises:
        ValueError: For malformed structures, missing fields, or duplicate IDs.
    """

    if not isinstance(warehouses, list):
        raise ValueError("warehouses must be a list of objects.")
    if not warehouses:
        raise ValueError("warehouses list cannot be empty.")

    warehouse_map: Dict[str, Coordinate] = {}
    for index, warehouse in enumerate(warehouses):
        if not isinstance(warehouse, dict):
            raise ValueError(f"Warehouse entry at index {index} must be an object.")

        warehouse_id = warehouse.get("id")
        if not warehouse_id:
            raise ValueError(f"Warehouse entry at index {index} is missing 'id'.")
        warehouse_key = str(warehouse_id)
        if warehouse_key in warehouse_map:
            raise ValueError(f"Duplicate warehouse ID detected: {warehouse_id}")

        location = _normalize_coordinate(warehouse.get("location"), f"warehouse '{warehouse_id}' location")
        warehouse_map[warehouse_key] = location

    return warehouse_map


def get_warehouse_by_id(warehouse_map: Mapping[str, Coordinate], warehouse_id: str) -> Coordinate:
    """Return a warehouse location by ID.

    Raises:
        ValueError: If the warehouse does not exist.
    """

    try:
        return warehouse_map[warehouse_id]
    except KeyError as exc:
        raise ValueError(f"Unknown warehouse ID: {warehouse_id}") from exc


def _get_agent_map(agents: Any) -> Dict[str, Coordinate]:
    """Convert agent records into an O(1) lookup map."""

    if not isinstance(agents, list):
        raise ValueError("agents must be a list of objects.")
    if not agents:
        raise ValueError("agents list cannot be empty.")

    agent_map: Dict[str, Coordinate] = {}
    for index, agent in enumerate(agents):
        if not isinstance(agent, dict):
            raise ValueError(f"Agent entry at index {index} must be an object.")

        agent_id = agent.get("id")
        if not agent_id:
            raise ValueError(f"Agent entry at index {index} is missing 'id'.")
        agent_key = str(agent_id)
        if agent_key in agent_map:
            raise ValueError(f"Duplicate agent ID detected: {agent_id}")

        location = _normalize_coordinate(agent.get("location"), f"agent '{agent_id}' location")
        agent_map[agent_key] = location

    return agent_map


def validate_data(data: Any) -> Dict[str, Any]:
    """Validate the JSON structure before simulation.

    The function validates warehouses and agents strictly because the simulator
    depends on them. Packages are checked for basic list/object structure here,
    while per-package field validation is handled during simulation so invalid
    packages can be skipped safely.
    """

    if not isinstance(data, dict):
        raise ValueError("Input data must be a JSON object.")

    required_keys = ("warehouses", "agents", "packages")
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

    warehouse_map = get_warehouse_map(data["warehouses"])
    agent_map = _get_agent_map(data["agents"])

    packages = data["packages"]
    if not isinstance(packages, list):
        raise ValueError("packages must be a list of objects.")

    return {
        "warehouses": warehouse_map,
        "agents": agent_map,
        "packages": packages,
    }


def find_nearest_agent(agent_positions: Mapping[str, Coordinate], warehouse_location: Sequence[float]) -> str:
    """Find the nearest agent to a warehouse location.

    Tie-breaking uses the lexicographically smaller agent ID.
    """

    if not agent_positions:
        raise ValueError("agents list cannot be empty.")

    nearest_agent_id: Optional[str] = None
    nearest_key: Optional[Tuple[float, str]] = None
    for agent_id, agent_location in agent_positions.items():
        distance = calculate_distance(agent_location, warehouse_location)
        candidate_key = (distance, agent_id)
        if nearest_key is None or candidate_key < nearest_key:
            nearest_key = candidate_key
            nearest_agent_id = agent_id

    assert nearest_agent_id is not None
    return nearest_agent_id


def _maybe_simulate_delay() -> float:
    """Optional bonus hook for a small randomized delivery delay."""

    if random.random() < 0.0:
        return round(random.uniform(0.1, 0.5), 2)
    return 0.0


def simulate_deliveries(data: Any) -> Dict[str, AgentState]:
    """Simulate one day of deliveries and return per-agent statistics."""

    validated = validate_data(data)
    warehouse_map = validated["warehouses"]
    agent_positions = dict(validated["agents"])
    packages = validated["packages"]

    agent_stats: Dict[str, AgentState] = {
        agent_id: AgentState(agent_id=agent_id, position=location)
        for agent_id, location in agent_positions.items()
    }
    seen_package_ids: set[str] = set()

    for index, package in enumerate(packages):
        if not isinstance(package, dict):
            LOGGER.warning("Skipping package at index %s: entry must be an object.", index)
            continue

        package_id = package.get("id")
        warehouse_id = package.get("warehouse_id")
        destination = package.get("destination")

        if not package_id:
            LOGGER.warning("Skipping package at index %s: missing 'id'.", index)
            continue
        if package_id in seen_package_ids:
            LOGGER.warning("Skipping duplicate package ID: %s", package_id)
            continue
        seen_package_ids.add(str(package_id))

        if not warehouse_id:
            LOGGER.warning("Skipping package %s: missing 'warehouse_id'.", package_id)
            continue

        try:
            warehouse_location = get_warehouse_by_id(warehouse_map, str(warehouse_id))
        except ValueError as exc:
            LOGGER.warning("Skipping package %s: %s", package_id, exc)
            continue

        try:
            destination_location = _normalize_coordinate(destination, f"package '{package_id}' destination")
        except ValueError as exc:
            LOGGER.warning("Skipping package %s: %s", package_id, exc)
            continue

        nearest_agent_id = find_nearest_agent(agent_positions, warehouse_location)
        current_agent_location = agent_positions[nearest_agent_id]

        travel_to_warehouse = calculate_distance(current_agent_location, warehouse_location)
        travel_to_destination = calculate_distance(warehouse_location, destination_location)
        total_trip_distance = travel_to_warehouse + travel_to_destination

        agent_positions[nearest_agent_id] = destination_location
        agent_stats[nearest_agent_id].position = destination_location
        agent_stats[nearest_agent_id].packages_delivered += 1
        agent_stats[nearest_agent_id].total_distance += total_trip_distance

        delay_minutes = _maybe_simulate_delay()
        if delay_minutes:
            LOGGER.info("Package %s experienced a simulated delay of %.2f minutes.", package_id, delay_minutes)

        LOGGER.info(
            "Package %s assigned to %s (warehouse %s -> destination %s).",
            package_id,
            nearest_agent_id,
            warehouse_id,
            destination_location,
        )

    return agent_stats


def _coerce_agent_stats(agent_stats: Mapping[str, Any]) -> Dict[str, AgentState]:
    """Allow generate_report to work with AgentState instances or dictionaries."""

    normalized: Dict[str, AgentState] = {}
    for agent_id, value in agent_stats.items():
        if isinstance(value, AgentState):
            normalized[agent_id] = value
            continue

        if not isinstance(value, Mapping):
            raise ValueError(f"Invalid agent statistics for {agent_id}.")

        normalized[agent_id] = AgentState(
            agent_id=agent_id,
            position=tuple(value.get("position", (0.0, 0.0)))[:2],
            packages_delivered=int(value.get("packages_delivered", 0)),
            total_distance=float(value.get("total_distance", 0.0)),
        )
    return normalized


def generate_report(agent_stats: Mapping[str, Any]) -> Dict[str, Any]:
    """Generate the final JSON-ready report payload."""

    normalized_stats = _coerce_agent_stats(agent_stats)
    report: Dict[str, Any] = {}
    best_agent_id: Optional[str] = None
    best_key: Optional[Tuple[float, int, str]] = None

    for agent_id in sorted(normalized_stats):
        stats = normalized_stats[agent_id]
        packages_delivered = stats.packages_delivered
        rounded_distance = round(stats.total_distance, 2)
        efficiency = round(stats.total_distance / packages_delivered, 2) if packages_delivered else 0.0

        report[agent_id] = {
            "packages_delivered": packages_delivered,
            "total_distance": rounded_distance,
            "efficiency": efficiency,
        }

        if packages_delivered > 0:
            candidate_key = (stats.total_distance / packages_delivered, -packages_delivered, agent_id)
            if best_key is None or candidate_key < best_key:
                best_key = candidate_key
                best_agent_id = agent_id

    report["best_agent"] = best_agent_id
    return report


def save_report(report: Mapping[str, Any], filepath: str | Path) -> None:
    """Write the final report JSON to disk."""

    path = Path(filepath)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def save_top_performer(report: Mapping[str, Any], filepath: str | Path = DEFAULT_CSV_FILE) -> None:
    """Export the best performer summary to CSV."""

    best_agent_id = report.get("best_agent")
    if not best_agent_id:
        return

    best_agent = report.get(best_agent_id)
    if not isinstance(best_agent, Mapping):
        return

    path = Path(filepath)
    with path.open("w", encoding="utf-8", newline="") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(["agent_id", "packages_delivered", "total_distance", "efficiency"])
        writer.writerow(
            [
                best_agent_id,
                best_agent.get("packages_delivered", 0),
                f"{float(best_agent.get('total_distance', 0.0)):.2f}",
                f"{float(best_agent.get('efficiency', 0.0)):.2f}",
            ]
        )


def _format_route_summary(agent_stats: Mapping[str, Any]) -> str:
    """Create a compact ASCII summary of the final agent routes."""

    lines: List[str] = ["FastBox route summary"]
    for agent_id in sorted(agent_stats):
        if agent_id == "best_agent":
            continue
        stats = agent_stats[agent_id]
        if isinstance(stats, Mapping):
            lines.append(
                f"{agent_id}: delivered={stats.get('packages_delivered', 0)} | distance={stats.get('total_distance', 0.0):.2f}"
            )
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for the application."""

    parser = argparse.ArgumentParser(description="FastBox Mystery Delivery System")
    parser.add_argument("data_file", nargs="?", default=str(DEFAULT_DATA_FILE), help="Path to data.json")
    parser.add_argument("--report-file", default=str(DEFAULT_REPORT_FILE), help="Path to report.json output")
    parser.add_argument("--csv-file", default=str(DEFAULT_CSV_FILE), help="Path to top_performer.csv output")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """CLI entry point used by both the script and the tests."""

    _configure_logging()
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    try:
        data = load_data(args.data_file)
        agent_stats = simulate_deliveries(data)
        report = generate_report(agent_stats)
        save_report(report, args.report_file)
        save_top_performer(report, args.csv_file)
    except (FileNotFoundError, ValueError) as exc:
        LOGGER.error("FastBox simulation failed: %s", exc)
        return 1

    delivered_total = sum(stat.packages_delivered for stat in agent_stats.values())
    total_requested = len(data.get("packages", [])) if isinstance(data.get("packages", []), list) else 0

    print("FastBox delivery simulation complete.")
    print(f"Packages delivered: {delivered_total}/{total_requested}")
    print(f"Best agent: {report['best_agent'] if report['best_agent'] is not None else 'None'}")
    print(f"Report saved to: {Path(args.report_file).resolve()}")
    print(f"Top performer CSV: {Path(args.csv_file).resolve()}")
    print(_format_route_summary(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())