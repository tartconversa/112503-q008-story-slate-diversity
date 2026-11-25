"""读取合成业务交接资料并核对表间关联。"""
import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "samples"

HEADERS = {'editions.csv': ['edition', 'work', 'rev', 'predecessor', 'submitted', 'ready_on', 'kind'], 'beats.csv': ['edition', 'beat', 'position', 'character', 'choice', 'event', 'ending'], 'readings.csv': ['fact', 'left_beat', 'right_beat', 'property', 'evidence', 'known_on'], 'lineage.csv': ['record', 'edition', 'source', 'field', 'authorization', 'confirmed_on'], 'airings.csv': ['broadcast', 'edition', 'channel', 'region', 'audience', 'on_day', 'theme'], 'slots.csv': ['slot', 'channel', 'region', 'day', 'units', 'limited_kind'], 'commitments.csv': ['commitment', 'work', 'edition', 'channel', 'slot', 'exclusive_to', 'state', 'at'], 'program_periods.csv': ['review', 'start', 'end', 'lookback_months', 'announced_floor', 'at']}
REFERENCES = [('beats.csv', 'edition', 'editions.csv', 'edition'), ('readings.csv', 'left_beat', 'beats.csv', 'beat'), ('readings.csv', 'right_beat', 'beats.csv', 'beat'), ('lineage.csv', 'edition', 'editions.csv', 'edition'), ('lineage.csv', 'source', 'editions.csv', 'edition'), ('airings.csv', 'edition', 'editions.csv', 'edition'), ('commitments.csv', 'slot', 'slots.csv', 'slot'), ('commitments.csv', 'edition', 'editions.csv', 'edition')]
OBSERVED_VALUES = [('editions.csv', 'work', 'W3', 2), ('commitments.csv', 'slot', 'S1', 2), ('airings.csv', 'edition', 'B1', 2)]

class SampleContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {}
        for name in HEADERS:
            with (DATA / name).open(encoding="utf-8", newline="") as source:
                reader = csv.DictReader(source, strict=True)
                if reader.fieldnames != HEADERS[name]:
                    raise ValueError(f"字段不一致：{name}")
                cls.sources[name] = list(reader)

    def test_tabular_structure(self):
        for name, rows in self.sources.items():
            with self.subTest(source=name):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_related_source_keys(self):
        for left, column, right, target in REFERENCES:
            with self.subTest(source=left, field=column):
                actual = {row[column] for row in self.sources[left] if row[column]}
                allowed = {row[target] for row in self.sources[right] if row[target]}
                self.assertTrue(actual)
                self.assertEqual(actual - allowed, set())

    def test_shared_or_revised_facts_have_source_rows(self):
        for name, column, value, minimum in OBSERVED_VALUES:
            with self.subTest(source=name, field=column, value=value):
                self.assertGreaterEqual(sum(row[column] == value for row in self.sources[name]), minimum)
