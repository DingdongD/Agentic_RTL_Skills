import unittest
from dse.pareto import frontier


class DseTests(unittest.TestCase):
    def test_dominated_and_unverified(self):
        def c(i, a, e, l, status="PASS"):
            return {"id": i, "area_um2": a, "energy_uj": e,
                    "latency_cycles": l, "verification": status, "evidence": "run.json"}
        result = frontier([c("a", 10, 10, 10), c("b", 12, 12, 12),
                           c("c", 8, 14, 9), c("d", 1, 1, 1, "NOT_RUN")])
        self.assertEqual([x["id"] for x in result["frontier"]], ["a", "c"])
        self.assertEqual(result["rejected"], 1)


if __name__ == "__main__":
    unittest.main()
