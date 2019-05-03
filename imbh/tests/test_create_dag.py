import unittest

from dag_creation.make_dag import create_dag_file, parse_args


class TestCreateDag(unittest.TestCase):
    def test_create_dag(self):
        args = parse_args(
            [
                "--jobs",
                "200",
                "--sub_fname",
                "inj_imbh_pe.sub",
                "--dag_fname",
                "tests/temp/test.dag",
            ]
        )
        create_dag_file(
            number_of_jobs=args.jobs,
            sub_filename=args.sub_fname,
            dag_filename=args.dag_fname,
        )
