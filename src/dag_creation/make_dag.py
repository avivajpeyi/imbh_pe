import argparse


"""
Usage:
python create_dag.py [--jobs NUM_JOBS] [--fname FNAME]

Creates NUM_JOBS injections and stores them in dag file FNAME
"""


def create_dag_file(number_of_jobs, dag_filename):
    file_handle = open(dag_filename, mode="+a")
    for i in range(0, number_of_jobs):
        job_text = f'Job {i} {dag_filename} \n VARS {i} jobNumber="{i}"\n'
        file_handle.write(job_text)
    file_handle.close()


def main():
    parser = argparse.ArgumentParser(description="dag file creator")
    parser.add_argument(
        "--jobs", "-j", default=5, type=int, help="number of jobs to be created"
    )
    parser.add_argument(
        "--fname", "-f", type=str, default="inj_imbh.dag", help="file name for output"
    )
    args = parser.parse_args()

    if not args.fname.endswith(".dag"):
        args.fname = args.fname + ".dag"

    create_dag_file(number_of_jobs=args.jobs, dag_filename=args.fname)


if __name__ == "__main__":
    main()
