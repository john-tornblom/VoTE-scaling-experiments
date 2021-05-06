#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

VOTE=$SCRIPTDIR/tools/vote
MODELS=$SCRIPTDIR/models
DATA=$SCRIPTDIR/data

mkdir -p $SCRIPTDIR/logs

sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.random-forest-25-5-gini.vote.log --job-name="T60.random-forest-25-5-gini.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --normalize --model $MODELS/random-forest-25-5-gini.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"
sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.catboost-75-5.vote.log --job-name="T60.catboost-75-5.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --model $MODELS/catboost-75-5.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"
sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.catboost-50-10.vote.log --job-name="T60.catboost-50-10.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --model $MODELS/catboost-50-10.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"
sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.random-forest-75-5-gini.vote.log --job-name="T60.random-forest-75-5-gini.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --normalize --model $MODELS/random-forest-75-5-gini.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"
sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.catboost-150-10.vote.log --job-name="T60.catboost-150-10.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --model $MODELS/catboost-150-10.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"
sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.random-forest-50-5-gini.vote.log --job-name="T60.random-forest-50-5-gini.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --normalize --model $MODELS/random-forest-50-5-gini.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"
sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.catboost-75-10.vote.log --job-name="T60.catboost-75-10.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --model $MODELS/catboost-75-10.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"
sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.random-forest-25-10-gini.vote.log --job-name="T60.random-forest-25-10-gini.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --normalize --model $MODELS/random-forest-25-10-gini.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"
sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.catboost-100-10.vote.log --job-name="T60.catboost-100-10.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --model $MODELS/catboost-100-10.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"
sbatch --exclusive -n1 -c1 -N1 -t 03:00:00 --output=logs/T60.random-forest-50-10-gini.vote.log --job-name="T60.random-forest-50-10-gini.vote" --wrap="/usr/bin/time -f '%es real, %Us user, %Ss kernel, %M mmem' $VOTE --normalize --model $MODELS/random-forest-50-10-gini.vote --margin 1 --timeout 60 --threads 1 $DATA/mnist.test.vote.csv"



