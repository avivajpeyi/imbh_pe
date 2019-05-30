# Steps to run

1. Install `bilby_pipe` 
2. Run `bilby_pipe_create_injection_file create_injection.ini` to generate the injection data stored in `outdir_imbh_injection/imbh_injection_injection_file.json`
3. Run `bilby_pipe injection_pe.ini --submit` to begin PE on the inejction data stored in `outdir_imbh_injection/imbh_injection_injection_file.json`


# Error in step 3
```
16:18 bilby_pipe INFO    : Prior-file set to imbh_injection_generation.prior
16:18 bilby_pipe INFO    : request_memory = 4 GB
16:18 bilby_pipe INFO    : request_memory_generation=8GB
16:18 bilby_pipe INFO    : request_cpus = 1

Traceback (most recent call last):
  File "/home/avi.vajpeyi/projects/imbh_pe/venv/bin/bilby_pipe", line 11, in <module>
    load_entry_point('bilby-pipe==0.1.0', 'console_scripts', 'bilby_pipe')()
  File "/home/avi.vajpeyi/projects/imbh_pe/venv/lib64/python3.6/site-packages/bilby_pipe-0.1.0-py3.6.egg/bilby_pipe/main.py", line 1107, in main
    Dag(inputs)
  File "/home/avi.vajpeyi/projects/imbh_pe/venv/lib64/python3.6/site-packages/bilby_pipe-0.1.0-py3.6.egg/bilby_pipe/main.py", line 398, in __init__
    raise BilbyPipeError("ini file contained no data-generation requirement")
bilby_pipe.utils.BilbyPipeError: ini file contained no data-generation requirement
```
