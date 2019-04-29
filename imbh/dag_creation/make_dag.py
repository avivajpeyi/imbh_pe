def create_dag_file(number_of_jobs: int, sub_filename: str, dag_filename: str):
    file_handle = open(dag_filename, mode="+a")
    for i in range(0, number_of_jobs):
        job_text = f'Job {i} {sub_filename} \n VARS {i} injectionNumber="{i}"\n'
        file_handle.write(job_text)
    file_handle.close()
