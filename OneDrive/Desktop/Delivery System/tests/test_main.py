import json
import tempfile
import unittest
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import main


class FastBoxTests(unittest.TestCase):
    def test_calculate_distance(self):
        self.assertAlmostEqual(main.calculate_distance((0, 0), (3, 4)), 5.0)

    def test_find_nearest_agent_uses_lexicographic_tie_break(self):
        agent_positions = {"A2": (0.0, 0.0), "A1": (0.0, 0.0)}
        result = main.find_nearest_agent(agent_positions, (10.0, 10.0))
        self.assertEqual(result, "A1")

    def test_simulation_updates_agent_position_between_packages(self):
        data = {
            "warehouses": [
                {"id": "W1", "location": [0, 0]}
            ],
            "agents": [
                {"id": "A1", "location": [0, 0]},
                {"id": "A2", "location": [10, 0]}
            ],
            "packages": [
                {"id": "P1", "warehouse_id": "W1", "destination": [100, 0]},
                {"id": "P2", "warehouse_id": "W1", "destination": [0, 0]}
            ]
        }

        agent_stats = main.simulate_deliveries(data)
        report = main.generate_report(agent_stats)

        self.assertEqual(agent_stats["A1"].packages_delivered, 1)
        self.assertEqual(agent_stats["A2"].packages_delivered, 1)
        self.assertEqual(report["best_agent"], "A2")

    def test_invalid_warehouse_package_is_skipped(self):
        data = {
            "warehouses": [
                {"id": "W1", "location": [0, 0]}
            ],
            "agents": [
                {"id": "A1", "location": [0, 0]}
            ],
            "packages": [
                {"id": "P1", "warehouse_id": "W9", "destination": [10, 10]}
            ]
        }

        agent_stats = main.simulate_deliveries(data)
        report = main.generate_report(agent_stats)

        self.assertEqual(agent_stats["A1"].packages_delivered, 0)
        self.assertEqual(report["best_agent"], None)

    def test_save_report_writes_json(self):
        report = {
            "A1": {"packages_delivered": 1, "total_distance": 10.0, "efficiency": 10.0},
            "best_agent": "A1",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "report.json"
            main.save_report(report, output_file)
            saved = json.loads(output_file.read_text(encoding="utf-8"))

        self.assertEqual(saved, report)

    def test_validate_data_rejects_missing_required_keys(self):
        with self.assertRaises(ValueError):
            main.validate_data({})


if __name__ == "__main__":
    unittest.main()
