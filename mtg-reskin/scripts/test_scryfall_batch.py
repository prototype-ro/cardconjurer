import unittest
from scryfall_batch import parse_decklist

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

if __name__ == "__main__":
    unittest.main()
