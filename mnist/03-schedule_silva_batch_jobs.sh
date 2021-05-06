#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

SILVA=$SCRIPTDIR/tools/silva
MODELS=$SCRIPTDIR/models
DATA=$SCRIPTDIR/data

mkdir -p $SCRIPTDIR/logs

sbatch --exclusive -n1 -c1 -N1 --mem=48gb -t 03:00:00 --output=logs/T60.catboost-100-10.silva.log --job-name="T60.catboost-100-10.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/catboost-100-10.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting softargmax"
sbatch --exclusive -n1 -c1 -N1 --mem=48gb -t 03:00:00 --output=logs/T60.catboost-75-10.silva.log --job-name="T60.catboost-75-10.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/catboost-75-10.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting softargmax"
sbatch --exclusive -n1 -c1 -N1 --mem=48gb -t 03:00:00 --output=logs/T60.catboost-75-5.silva.log --job-name="T60.catboost-75-5.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/catboost-75-5.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting softargmax"
sbatch --exclusive -n1 -c1 -N1 --mem=48gb -t 03:00:00 --output=logs/T60.catboost-150-10.silva.log --job-name="T60.catboost-150-10.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/catboost-150-10.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting softargmax"
sbatch --exclusive -n1 -c1 -N1 --mem=48gb -t 03:00:00 --output=logs/T60.catboost-50-10.silva.log --job-name="T60.catboost-50-10.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/catboost-50-10.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting softargmax"
sbatch --exclusive -n1 -c1 -N1 --mem=90gb -t 03:00:00 --output=logs/T60.random-forest-50-10-gini.silva.log --job-name="T60.random-forest-50-10-gini.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/random-forest-50-10-gini.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting average"
sbatch --exclusive -n1 -c1 -N1 --mem=90gb -t 03:00:00 --output=logs/T60.random-forest-75-5-gini.silva.log --job-name="T60.random-forest-75-5-gini.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/random-forest-75-5-gini.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting average"
sbatch --exclusive -n1 -c1 -N1 --mem=90gb -t 03:00:00 --output=logs/T60.random-forest-50-5-gini.silva.log --job-name="T60.random-forest-50-5-gini.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/random-forest-50-5-gini.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting average"
sbatch --exclusive -n1 -c1 -N1 --mem=48gb -t 03:00:00 --output=logs/T60.random-forest-25-5-gini.silva.log --job-name="T60.random-forest-25-5-gini.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/random-forest-25-5-gini.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting average"
sbatch --exclusive -n1 -c1 -N1 --mem=48gb -t 03:00:00 --output=logs/T60.random-forest-25-10-gini.silva.log --job-name="T60.random-forest-25-10-gini.silva" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $SILVA $MODELS/random-forest-25-10-gini.silva $DATA/mnist.test.silva.csv --perturbation l_inf 1 --sample-timeout 60 --voting average"
