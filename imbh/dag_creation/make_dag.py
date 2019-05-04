import argparse

from tools.file_utils import IncorrectFileType


def create_dag_file(number_of_jobs: int, sub_filename: str, dag_filename: str):
    file_handle = open(dag_filename, mode="w")
    for i in range(0, number_of_jobs):
        job_text = 'Job {} {} \n VARS {} injectionNumber="{}"\n'.format(
            i, sub_filename, i, i
        )
        file_handle.write(job_text)
    file_handle.close()


def parse_args(args):
    parser = argparse.ArgumentParser(description="dag file creator")
    required = parser.add_argument_group("required named arguments")
    required.add_argument(
        "--jobs", "-j", default=200, type=int, help="number of jobs to be created"
    )
    required.add_argument("--dag_fname", "-d", type=str, help="dag output filename")
    required.add_argument("--sub_fname", "-s", type=str, help="subfile to run job")

    args = parser.parse_args(args)

    if not args.dag_fname.endswith(".dag"):
        raise IncorrectFileType(
            "Dag file doenst end with '.dag': {}".format(args.dag_fname)
        )

    if not args.sub_fname.endswith(".sub"):
        raise IncorrectFileType(
            "Sub file doenst end with '.sub': {}".format(args.sub_fname)
        )

    return args
