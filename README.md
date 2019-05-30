# IMBH Parameter Estimation

## Posterior Prob of a signal hypothesis
- Generate a list of IMBH GW parameters and use them to simulate GW signals.
- Inject simulated signals into LIGO noise data.
- Use a nested sampling to generate a list of posterior samples of
potential IMBH parameters based on the hypothesis that *data=noise+signal*.
- The posterior samples give us
    - *p(θ|d)* posterior of parameters given the data
    - *p(θ<sub>i</sub>|d)* marginalised posteriors for our parameters
    - *Z* (evidence of the hypothesis)

## Population Inference
- Calculate *p(θ|d)* and *Z* for several injected signals
- Use the numerous *p(θ|d)* to begin collecting a list of population posterior density
samples, based on a population model hypothesis
- Use population posterior density samples to marginalise hyper-parameters:
    - *Duty-cycle*: % of data that is modeled well by the current hypothesis d=n+s
    - Mass distribution
    - Spin distribution

## Distributions to give prior info to future detections
- Mass, spin, duty cycle marginalised posteriors provide an idea of how probable
certain events are



