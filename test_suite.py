import unittest
import transformation

# Simple test suite with a demo test case

class PipelineTests(unittest.TestCase):
    def test_get_character_info(self):
        # Checks that the results dictionary is not empty
        info_categories = ["powerstats", "appearance"]
        character_id = "247"
        self.assertTrue(transformation.get_character_info(character_id=character_id, info_categories=info_categories))

if __name__ == '__main__':
    unittest.main()