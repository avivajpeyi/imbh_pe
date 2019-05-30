
---
![](https://placehold.it/350x90/009955/fff?text=Side-Projects)

## Initial IMBH
simulate IMBH GW signals and then injecting signals into LIGO data with noise.
Analysing data with Bayseian Inference and




It’s interesting. I see this as a jumping off point to test the following two hypotheses:
1) is this the best we can measure the individual masses because the signals are so short
2) Are we doing a bad job of sampling the masses? In which case we might do better by sampling in chirp mass and mass ratio (instead of the component masses)

Rory Smith   [21 minutes ago]
A positive answer to either would be interesting. For 1) we can show that it’s hard to do precision astrophysics with IMBHBs form 20Hz so we might need to go to lower frequencies. For 2) if it turns out that we can measure the chirp mass better than the component masses, then great!

Avi Vajpeyi   [14 minutes ago]
ok!

1) How can we know that this is the best we can measure the individual masses?

2) Ok! So should I get rid of m1 and m2 from the prior files and replace them with M_chirp and q?

Rory Smith   [13 minutes ago]
Yep

Rory Smith   [13 minutes ago]
I think you have to add the following to the instantiation of the likelihood `mass_parameter='chirp_mass'`

Rory Smith   [12 minutes ago]
The answer to 1) is simple: because you’re using the correct model for the signal and noise the posterior pdfs on the masses must be unbiased. Whatever comes out is by definition the best measurement you can make on those parameters

Rory Smith   [12 minutes ago]
Now, we can of course go a little deeper. The signals are very short in duration from 20Hz and we’d see more signal from, e.g., 10Hz. This is another avenue that could be explored

