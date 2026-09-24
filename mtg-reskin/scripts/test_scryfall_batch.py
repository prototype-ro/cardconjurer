import unittest
from unittest.mock import patch
from scryfall_batch import parse_decklist, enrich_decklist

class TestParseDecklist(unittest.TestCase):
    def test_parses_quantity_and_name(self):
        text = "1 Sol Ring\n2 Swamp\n1 Kaalia of the Vast"
        result = parse_decklist(text)
        self.assertEqual(
            result,
            [
                {"quantity": 1, "name": "Sol Ring"},
                {"quantity": 2, "name": "Swamp"},
                {"quantity": 1, "name": "Kaalia of the Vast"},
            ],
        )

    def test_skips_blank_lines_and_comments(self):
        text = "1 Sol Ring\n\n// Commander\n1 Kaalia of the Vast\n"
        result = parse_decklist(text)
        self.assertEqual(
            result,
            [
                {"quantity": 1, "name": "Sol Ring"},
                {"quantity": 1, "name": "Kaalia of the Vast"},
            ],
        )

from scryfall_batch import chunk_identifiers

class TestChunkIdentifiers(unittest.TestCase):
    def test_chunks_into_groups_of_75(self):
        names = [{"name": f"Card {i}"} for i in range(160)]
        chunks = list(chunk_identifiers(names))
        self.assertEqual(len(chunks), 3)
        self.assertEqual(len(chunks[0]), 75)
        self.assertEqual(len(chunks[1]), 75)
        self.assertEqual(len(chunks[2]), 10)

class TestEnrichDecklist(unittest.TestCase):
    @patch("scryfall_batch.fetch_collection")
    def test_preserves_order_and_quantity_defaults_missing_and_matches_case_insensitively(
        self, mock_fetch
    ):
        decklist = "1 Sol Ring\n2 Swamp\n1 Kaalia of the Vast"
        # Scryfall returns names in a different order/case, and omits Swamp
        # entirely (simulating a card not found in the response).
        mock_fetch.return_value = [
            {
                "name": "Kaalia of the Vast",
                "type_line": "Legendary Creature — Human Cleric",
                "color_identity": ["B", "R", "W"],
                "cmc": 4.0,
                "oracle_text": "Flying",
                "keywords": ["Flying"],
            },
            {
                "name": "SOL RING",
                "type_line": "Artifact",
                "color_identity": [],
                "cmc": 1.0,
                "oracle_text": "{T}: Add {C}{C}.",
                "keywords": [],
            },
        ]

        result = enrich_decklist(decklist)

        self.assertEqual(len(result), 3)

        # Order/quantity preserved from the original decklist.
        self.assertEqual(result[0]["name"], "Sol Ring")
        self.assertEqual(result[0]["quantity"], 1)
        self.assertEqual(result[1]["name"], "Swamp")
        self.assertEqual(result[1]["quantity"], 2)
        self.assertEqual(result[2]["name"], "Kaalia of the Vast")
        self.assertEqual(result[2]["quantity"], 1)

        # Case-insensitive name matching: "Sol Ring" matched "SOL RING".
        self.assertEqual(result[0]["type_line"], "Artifact")
        self.assertEqual(result[0]["mana_value"], 1.0)

        # Card missing from the mocked response gets defaulted empty fields.
        self.assertEqual(result[1]["type_line"], "")
        self.assertEqual(result[1]["color_identity"], [])
        self.assertIsNone(result[1]["mana_value"])
        self.assertEqual(result[1]["oracle_text"], "")
        self.assertEqual(result[1]["keywords"], [])

        # Matched card retains its enriched fields.
        self.assertEqual(
            result[2]["type_line"], "Legendary Creature — Human Cleric"
        )
        self.assertEqual(result[2]["color_identity"], ["B", "R", "W"])


if __name__ == "__main__":
    unittest.main()
