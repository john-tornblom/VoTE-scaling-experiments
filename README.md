# Scalability of Formal Verifiers for Tree Ensembles

This repository contains the source code and data used to demonstrate the
application of the tool [VoTE][vote] in two case studies, namely a digit
recognition and aircraft collision avoidance. For more information, see
[Scaling up Memory-Efficient Formal Verification Tools for Tree Ensembles][paper].

## ACAS Xu Case Study
On Ubuntu-flavored operating systems, you can invoke the following commands to
install dependencies, compile the source code, and run the experiments.

```console
john@localhost:$ sudo apt-get install autoconf libtool build-essential python-cffi
john@localhost:$ python -m pip install catboost --user
john@localhost:$ git clone --recurse-submodules https://github.com/john-tornblom/VoTE-scaling-experiments
john@localhost:$ ./acasxu/01-compile-verifier.sh
john@localhost:$ ./acasxu/01-train-models.sh
john@localhost:$ ./acasxu/02-verify-properties.sh
john@localhost:$ ./acasxu/03-extract-results.sh
john@localhost:$ cat acasxu/results.csv
```

## MNIST Case Study
This case study was designed to run on a [SLURM][slurm] cluster. Assuming you
have a SLURM client installed and configured on your system, the following set
of commands can be used to run the experiments.
```console
john@localhost:$ sudo apt-get install autoconf libtool build-essential
john@localhost:$ git clone --recurse-submodules https://github.com/john-tornblom/VoTE-scaling-experiments
john@localhost:$ ./mnist/01-compile-verifiers.sh
john@localhost:$ ./mnist/01-translation_validation.sh
john@localhost:$ ./mnist/02-create_vote_models.sh
john@localhost:$ ./mnist/03-schedule_silva_batch_jobs.sh   # depends on slurm
john@localhost:$ ./mnist/03-schedule_vote_batch_jobs.sh    # depends on slurm
john@localhost:$ ./mnist/03-schedule_vote-mc_batch_jobs.sh # depends on slurm
john@localhost:$ ./mnist/04-extract-results.py
john@localhost:$ cat mnist/T60.GB.csv
```

[vote]: https://github.com/john-tornblom/VoTE
[paper]: https://github.com/john-tornblom/VoTE
[slurm]: https://slurm.schedmd.com



