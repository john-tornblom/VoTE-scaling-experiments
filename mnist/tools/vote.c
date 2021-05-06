#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <string.h>
#include <math.h>
#include <assert.h>
#include <time.h>
#include <argp.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <vote.h>

// copied from vote_tree.h
struct vote_tree {
  int* left;
  int* right;
  
  int*     feature;
  real_t*  threshold;
  real_t** value;

  size_t nb_inputs;
  size_t nb_outputs;
  size_t nb_nodes;
};


typedef struct sample_analysis {
  vote_ensemble_t *ensemble;
  real_t margin;
  real_t timeout;
  real_t *sample;
  size_t sample_predicted;
  size_t label;
  
  struct timespec start_clock;
  struct timespec stop_clock;

  vote_outcome_t outcome;
} sample_analysis_t;


typedef struct dataset {
  size_t nb_rows;
  size_t nb_cols;
  real_t *data;
} dataset_t;


typedef struct dataset_analysis {
  vote_ensemble_t *ensemble;
  real_t sample_timeout;
  real_t margin;
  size_t threads;
  dataset_t dataset;
  bool normalize;
} dataset_analysis_t;


typedef void (workqueue_cb_t)(void *ctx);


typedef struct task {
  workqueue_cb_t *cb;
  void *ctx;
  struct task *next;
} task_t;


typedef struct workqueue {
  task_t *queue;
  pthread_mutex_t lock;
} workqueue_t;


static task_t* workqueue_pop_task(workqueue_t *wq) {
  pthread_mutex_lock(&wq->lock);

  task_t *task = wq->queue;
  if(task) {
    wq->queue = task->next;
  }

  pthread_mutex_unlock(&wq->lock);

  return task;
}


static void* workqueue_thread(void *ctx) {
  task_t *task;
  workqueue_t* wq = (workqueue_t*)ctx;

  while((task = workqueue_pop_task(wq))) {
    task->cb(task->ctx);
  }
  
  pthread_exit(NULL);
  return NULL;
}


static workqueue_t *workqueue_new() {
  workqueue_t* wq = calloc(1, sizeof(workqueue_t));
  assert(wq);

  pthread_mutex_init(&wq->lock, NULL);
  
  return wq;
}


static void workqueue_del(workqueue_t* wq) {
  task_t* next;
  
  while(wq->queue) {
    next = wq->queue->next;
    free(wq->queue);
    wq->queue = next;
  }
  
  free(wq);
}


static void workqueue_launch(workqueue_t* wq, unsigned short nb_threads) {
  pthread_t threads[nb_threads];

  for(size_t i=0; i<nb_threads; i++) {
    pthread_create(&threads[i], NULL, workqueue_thread, wq);
  }

  for(size_t i=0; i<nb_threads; i++) {
    pthread_join(threads[i], NULL);
  }
}


static void workqueue_schedule(workqueue_t *wq, workqueue_cb_t *cb, void *ctx) {
  task_t* task = calloc(1, sizeof(task_t));
  assert(task);

  task->cb   = cb;
  task->ctx  = ctx;

  pthread_mutex_lock(&wq->lock);
  task->next = wq->queue;
  wq->queue = task;
  pthread_mutex_unlock(&wq->lock);
}


static void normalize(double* vec, size_t length) {
  double sum = 0;

  for(size_t i=0; i<length; i++) {
    sum += vec[i];
  }

  assert(sum != 0);
  
  for(size_t i=0; i<length; i++) {
    vec[i] /= sum;
  }
}


static real_t timespec_diff(struct timespec *start, struct timespec *stop) {
  real_t sec = 0;
  real_t nsec = 0;

  if((stop->tv_nsec - start->tv_nsec) < 0) {
    sec = (real_t)stop->tv_sec - start->tv_sec - 1;
    nsec = (real_t)stop->tv_nsec - start->tv_nsec + 1000000000;
  } else {
    sec = (real_t)stop->tv_sec - start->tv_sec;
    nsec = (real_t)stop->tv_nsec - start->tv_nsec;
  }
  
  return sec + (nsec / 1e9);
}


static vote_outcome_t is_correct(void *ctx, vote_mapping_t *m) {
  struct timespec curr_clock;
  sample_analysis_t *a = (sample_analysis_t*)ctx;
  
  clock_gettime(CLOCK_THREAD_CPUTIME_ID, &curr_clock);
  
  if(timespec_diff(&a->start_clock, &curr_clock) > a->timeout) {
    a->outcome = VOTE_UNSURE;
    return VOTE_FAIL;
  }

  a->outcome = vote_mapping_check_argmax(m, a->sample_predicted);

  return a->outcome;
}


static void run_analysis_on_sample(void* ctx) {
  sample_analysis_t *a = (sample_analysis_t*)ctx;
  vote_bound_t bounds[a->ensemble->nb_inputs];

  clock_gettime(CLOCK_THREAD_CPUTIME_ID, &a->start_clock);
  
  for(size_t i=0; i<a->ensemble->nb_inputs; i++) {
    bounds[i].lower = a->sample[i] - a->margin;
    bounds[i].upper = a->sample[i] + a->margin;
  }

  vote_ensemble_absref(a->ensemble, bounds, is_correct, a);

  clock_gettime(CLOCK_THREAD_CPUTIME_ID, &a->stop_clock);
}


static void run_analysis_on_dataset(dataset_analysis_t *a) {
  size_t nb_samples = a->dataset.nb_rows;
  sample_analysis_t analyses[nb_samples];
  workqueue_t *wq = workqueue_new();
  struct timespec start_clock;
  struct timespec stop_clock;
  real_t pred[a->ensemble->nb_outputs];
  
  for(size_t row=0; row<nb_samples; row++) {
    analyses[row].ensemble = a->ensemble;
    analyses[row].margin = a->margin;
    analyses[row].timeout = a->sample_timeout;
    
    analyses[row].sample = &a->dataset.data[row * a->dataset.nb_cols];
    analyses[row].label = (size_t)roundf(analyses[row].sample[a->ensemble->nb_inputs]);

    vote_ensemble_eval(a->ensemble, analyses[row].sample, pred);
    analyses[row].sample_predicted = (size_t)vote_argmax(pred, a->ensemble->nb_outputs);

    workqueue_schedule(wq, run_analysis_on_sample, &analyses[row]);
  }

  clock_gettime(CLOCK_REALTIME, &start_clock);
  workqueue_launch(wq, a->threads);
  clock_gettime(CLOCK_REALTIME, &stop_clock);

  size_t robust = 0;
  size_t fragile = 0;
  size_t vulnerable = 0;
  size_t break_ = 0;
  size_t timeouts = 0;
  real_t walltime = timespec_diff(&start_clock, &stop_clock);
  
  for(size_t row=0; row<nb_samples; row++) {
    bool stable = analyses[row].outcome == VOTE_PASS;
    bool correct = analyses[row].label == analyses[row].sample_predicted;
    
    robust += (correct && stable);
    fragile += (correct && !stable);
    vulnerable += (!correct && stable);
    break_ += (!correct && !stable);
    timeouts += analyses[row].outcome == VOTE_UNSURE;
  }
  
  printf("margin:     %g\n", a->margin);
  printf("timeout:    %gs\n", a->sample_timeout);
  printf("nb_inputs:  %ld\n", a->ensemble->nb_inputs);
  printf("nb_outputs: %ld\n", a->ensemble->nb_outputs);
  printf("nb_trees:   %ld\n", a->ensemble->nb_trees);
  printf("nb_nodes:   %ld\n", a->ensemble->nb_nodes);
  printf("robust:     %ld\n", robust);
  printf("fragile:    %ld\n", fragile);
  printf("vulnerable: %ld\n", vulnerable);
  printf("break:      %ld\n", break_);
  printf("timeouts:   %ld\n", timeouts);
  printf("runtime:    %gs\n", walltime);

  workqueue_del(wq);
}


static error_t parse_cb(int key, char *arg, struct argp_state *state) {
  dataset_analysis_t *a = state->input;
  
  switch(key) {
  case 'm': //model
    if(!(a->ensemble = vote_ensemble_load_file(arg))) {
      fprintf(stderr, "Unable to load model from %s\n", arg);
      return ARGP_ERR_UNKNOWN;
    }
    break;

  case 'M': //margin
    a->margin = atof(arg);
    break;

  case 'n': //normalize
    a->normalize = 1;
    break;
    
  case 'T': //timeout
    a->sample_timeout = atof(arg);
    break;

  case 't': //threads
    a->threads = atoi(arg);
    break;
    
  case ARGP_KEY_ARG: //CSV_FILE
    if(!vote_csv_load(arg, &a->dataset.data, &a->dataset.nb_rows,
		      &a->dataset.nb_cols)) {
      fprintf(stderr, "Unable to load data from %s\n", arg);
      exit(1);
    } 
    break;

  case ARGP_KEY_END:
    if(state->arg_num < 1) {
      argp_usage(state);
    }
    break;
    
  default:
    return ARGP_ERR_UNKNOWN;
  }

  return 0;
}
  

int main(int argc, char** argv) {
  struct argp_option opts[] = {
    {.name="model", .key='m', .arg="PATH",
     .doc="Path to a serialized tree-based classifier"},

    {.name="margin", .key='M', .arg="NUMBER",
     .doc="The additive margin to which the classifier should be robust against"},
    
    {.name="normalize", .key='n',
     .doc="Normalize leaves"},
    
    {.name="threads", .key='t', .arg="NUMBER",
     .doc="Perform analyses concurrently on a given NUMBER of threads"},
    
    {.name="timeout", .key='T', .arg="NUMBER",
     .doc="Timeout the analysis of a sample after NUMBER of seconds"},

    {0}
  };
  
  struct argp argp = {
    .parser   = parse_cb,
    .doc      = "Verify the robustness of a tree-based classifier against input "
                "perturbations to a set of samples stored in the CSV format.",
    .args_doc = "CSV_FILE",
    .options  = opts
  };

  struct dataset_analysis a = {
    .sample_timeout = UINT_MAX,
    .threads = sysconf(_SC_NPROCESSORS_ONLN)
  };
    
  if(argp_parse(&argp, argc, argv, 0, 0, &a)) {
    exit(1);
  }

  if(a.normalize) {
    for(size_t i=0; i<a.ensemble->nb_trees; i++) {
      vote_tree_t *t = a.ensemble->trees[i];
      for(size_t j=0; j<t->nb_nodes; j++) {
	normalize(t->value[j], t->nb_outputs);
      }
    }
  }
  
  run_analysis_on_dataset(&a);

  if(a.ensemble) {
    vote_ensemble_del(a.ensemble);
  }
}


const char *argp_program_version = "0.1";
const char *argp_program_bug_address = "";


