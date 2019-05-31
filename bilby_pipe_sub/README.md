# Steps to run

1. Install `bilby_pipe` 
2. Run `bilby_pipe_create_injection_file create_injection.ini` to generate the injection data stored in `outdir_imbh_injection/imbh_injection_injection_file.json`
3. Run `bilby_pipe injection_pe.ini` to begin PE on the inejction data stored in `outdir_imbh_injection/imbh_injection_injection_file.json`


# Error in step 3
```
18:07 bilby_pipe INFO    : Running bilby_pipe version: 0.1.0: (CLEAN) 1bbacbd 2019-05-28 21:49:12 -0700
18:07 bilby INFO    : Running bilby version: 0.5.0:
18:07 bilby DEBUG   : DISPLAY=localhost:10.0 environment found
18:07 bilby WARNING : You do not have gwpy installed currently. You will  not be able to use some of the prebuilt functions.
18:07 bilby WARNING : You do not have gwpy installed currently. You will  not be able to use some of the prebuilt functions.
18:07 bilby WARNING : You do not have gwpy installed currently. You will  not be able to use some of the prebuilt functions.
18:07 bilby_pipe DEBUG   : Creating new Input object
18:07 bilby_pipe INFO    : Command line arguments: Namespace(X509=None, accounting='ligo.dev.o3.cbc.pe.lalinference', calibration_model=None, channel_dict=None, coherence_test=False, create_plots=True, create_summary=True, data_dict=None, data_format=None, default_prior='BBHPriorDict', deltaT=0.2, detectors=['H1', 'L1'], distance_marginalization=True, distance_marginalization_lookup_table=None, duration=4.0, email='avi.vajpeyi@gmail.com', existing_dir=None, frequency_domain_source_model='lal_binary_black_hole', gaussian_noise=True, generation_seed=None, gps_file=None, gracedb=None, gracedb_url=None, ini='injection_pe.ini', injection=True, injection_file='outdir_imbh_injection/imbh_injection_injection_file.json', label='imbh_injection', likelihood_type='GravitationalWaveTransient', local=False, local_generation=False, maximum_frequency=None, minimum_frequency='20', n_injection=None, n_parallel=1, outdir='outdir_imbh_injection', periodic_restart_time=10800, phase_marginalization=False, post_trigger_duration=2, postprocessing_arguments=None, postprocessing_executable=None, prior_file='imbh_injection_generation.prior', psd_dict=None, psd_fractional_overlap=0.5, psd_length=32, psd_method='median', psd_start_time=None, reference_frequency=20, request_cpus=1, request_memory=4, request_memory_generation=None, roq_folder=None, roq_scale_factor=1, sampler=['dynesty'], sampler_kwargs=None, sampling_frequency=4096, sampling_seed=None, singularity_image=None, spline_calibration_amplitude_uncertainty_dict=None, spline_calibration_envelope_dict=None, spline_calibration_nodes=5, spline_calibration_phase_uncertainty_dict=None, submit=True, time_marginalization=True, transfer_files=False, trigger_time=None, tukey_roll_off=0.4, verbose=True, waveform_approximant='IMRPhenomPv2', webdir='/home/avi.vajpeyi/public_html/bilby_pipe_imbh_results', zero_noise=False)
18:07 bilby_pipe DEBUG   : Known detector list = ['H1', 'L1', 'V1']
18:07 bilby_pipe DEBUG   : Setting use_singularity=False
18:07 bilby_pipe DEBUG   : Directory outdir_imbh_injection exists
18:07 bilby_pipe DEBUG   : Directory outdir_imbh_injection/submit exists
18:07 bilby_pipe DEBUG   : Directory outdir_imbh_injection/log_data_generation exists
18:07 bilby_pipe DEBUG   : Directory outdir_imbh_injection/log_data_analysis exists
18:07 bilby_pipe DEBUG   : Directory outdir_imbh_injection/data exists
18:07 bilby_pipe DEBUG   : Directory outdir_imbh_injection/log_results_page exists
18:07 bilby_pipe DEBUG   : Directory outdir_imbh_injection/result exists
18:07 bilby_pipe INFO    : Setting segment duration 4.0
18:07 bilby_pipe INFO    : Prior-file set to imbh_injection_generation.prior
18:07 bilby_pipe INFO    : request_memory = 4 GB
18:07 bilby_pipe INFO    : request_memory_generation=8GB
18:07 bilby_pipe INFO    : request_cpus = 1
Traceback (most recent call last):
  File "/home/avi.vajpeyi/projects/imbh_pe/venv/bin/bilby_pipe", line 11, in <module>
    load_entry_point('bilby-pipe==0.1.0', 'console_scripts', 'bilby_pipe')()
  File "/home/avi.vajpeyi/projects/imbh_pe/venv/lib64/python3.6/site-packages/bilby_pipe-0.1.0-py3.6.egg/bilby_pipe/main.py", line 1107, in main
    Dag(inputs)
  File "/home/avi.vajpeyi/projects/imbh_pe/venv/lib64/python3.6/site-packages/bilby_pipe-0.1.0-py3.6.egg/bilby_pipe/main.py", line 398, in __init__
    raise BilbyPipeError("ini file contained no data-generation requirement")
bilby_pipe.utils.BilbyPipeError: ini file contained no data-generation requirement
```


Modules installed in `venv`
```
asn1crypto==0.24.0
astropy==3.1.2
attrs==19.1.0
bilby==0.5.0
bilby-pipe==0.1.0
certifi==2019.3.9
cffi==1.12.3
chardet==3.0.4
Click==7.0
ConfigArgParse==0.14.0
corner==2.0.1
cryptography==2.6.1
cycler==0.10.0
decorator==4.4.0
deepdish==0.3.6
dill==0.2.9
dqsegdb2==1.0.1
dynesty==0.9.5.3
future==0.17.1
gwdatafind==1.0.4
gwosc==0.4.3
gwpy==0.15.0
h5py==2.9.0
hurry.filesize==0.9
idna==2.8
ipython-genutils==0.2.0
jsonschema==3.0.1
jupyter-core==4.4.0
kiwisolver==1.1.0
lalsuite==6.57
ligo-gracedb==2.2.2
ligo-segments==1.2.0
ligotimegps==2.0.1
lscsoft-glue==2.0.0
matplotlib==3.1.0
mock==3.0.5
nbformat==4.4.0
numexpr==2.6.9
numpy==1.16.4
opencv-python-headless==4.1.0.25
pandas==0.24.2
plotly==3.9.0
PyCondor==0.5.0
pycparser==2.19
pyOpenSSL==19.0.0
pyparsing==2.4.0
pyrsistent==0.15.2
python-dateutil==2.8.0
pytz==2019.1
requests==2.22.0
retrying==1.3.3
scipy==1.3.0
six==1.12.0
tables==3.5.1
Theano==1.0.4
tqdm==4.32.1
traitlets==4.3.2
typing==3.6.6
urllib3==1.25.3
```
