import argparse
import unittest
from unittest import mock

# import imbh
import imbh.summarise_pe_results as summarise_pe_results

# from imbh.imbh_pe_calculator import pe_results_summary


class TestPeSummary(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            results="imbh/tests/pe_test/H1L1-injection1/H1L1_injection1_result.json"
        ),
    )
    def test_main_runner(self, mock_args):
        summarise_pe_results.main()
        pass

    def test_get_url_from_path(self):
        pass
