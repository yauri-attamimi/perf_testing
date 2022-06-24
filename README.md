# Moove Backend API Performance Testing Scripts

This repository holds test infrastructure and benchmarks used to test Moove's Backend Service APIs.

# Author

Yauri Attamimi

# Maintainer(s)

- [Yauri Attamimi](mailto:yauri.attamimi@moove.io)

# Contents

- [Glossary](#glossary)
- [Structure of repository](#structure-of-repository)
- [Build and test](#build-and-test)
  - [Build requirements](#build-requirements)
  - [How to build](#how-to-build)
  - [Testing Scripts Configuration](#testing-scripts-configuration)
  - [Running Performance Tests](#running-performance-tests)
    - [Experiment tags](#experiment-tags) 
    - [Experiment results](#experiment-results)
    - [Outputs](#outputs) 

# Glossary

*Performance test* is measurement of execution of a target command line executable file for specific input file with certain command line parameters.
For example, a performance test for Driver App APIs is execution of `app.py` within the `driver` package for the given parameters as defined within respective `yaml` files within each folder that represent our target environment.

An input file is called *benchmark*. This is the `yaml` file we utilize to specify different scenario parameters for **load testing**, **stress testing**, **spike testing**, and **soak testing**.

An *experiment* is a set of performance tests for a single target executable, same command line parameters and run for multiple benchmarks located in the predefined directory.

Regular experiments allow to track how changes in the source codes affect the target executable performance on same set of benchmarks. 

A *domain* determines specific settings for a certain target executable, such as input file extensions, command line syntax, how to interpret input and output of program run,
how to analyse and aggregate multiple runs. 
Here an example of *domain* would be our `driver` folder (a.k.a. package). We use this `driver` folder to group all of our testing script resources for our Driver App. 


# Structure of repository

* `venv` is a virtual environment which is used to isolate all of our python dependencies for the performance testing scripts.
* `driver` is our testing module for all APIs used by the DriverApp. Other modules should have their own respective folder at the same level with this particular driver folder.
* `driver/staging` contains our testing configuration scripts used against our staging environment. You should create another folder (at the same level with this `staging` folder) if you'd like to have different target environment (e.g. `driver/production` for **production** testing).
* `driver/util` contains some util/common scripts used in our main testing scripts. 
* `driver/app.py` contains all main testing scripts for DriverApp APIs.


# Build and test 

## Build requirements

* **Python 3.9+**

If you don't have Python 3.9+, you can download it from [here](https://www.python.org/downloads/release/python-390/).

Mac users can also use `brew` to install it. Find the instructions [here](https://docs.python-guide.org/starting/install3/osx/). 

## How to build

1. Open your console terminal (or command prompt for Windows).
2. Go into the parent directory of this project : `cd perf_testing`
3. Activate **virtual environment** : `source venv/bin/activate`
4. Install all dependencies : `pip install -r requirements.txt`

## Testing scripts configuration

Configuration of the performance test infrastructure is represented as a bunch of files located within a folder that represent our target environment. 
E.g. `staging` is meant to be used for testing our **staging** environment, `prod` is meant for testing our **production** environment, etc.

It includes:
* Testing Data in the format of a CSV file. E.g. `data.csv`.
* Different config files for different testing scenarios, i.e. **load**, **stress**, **spike**, and **soak**.

## Running performance tests

In a nutshell, we use `locust` to run our main performance testing script. 

We conventionally named our main performance testing script as `app.py`, and it's located within our `domain` folder/package. 

Following are some examples on how we run different performance testing scenarios using different test configuration files hosted in our `staging` folder.

### Load Testing

```shell
cd driver && locust -f app.py --config staging/load_config.yaml
```

### Stress Testing

```shell
cd driver && locust -f app.py --config staging/stress_config.yaml
```

### Spike Testing

```shell
cd driver && locust -f app.py --config staging/spike_config.yaml
```

### Soak Testing

```shell
cd driver && locust -f app.py --config staging/soak_config.yaml
```

### Experiment tags

In order to run some of the scripts, `locust` can filter out or identifies experiments by tag(s).

Here are some examples on how we utilize this tag features:

#### Run all Stories

```shell
cd driver && locust -f app.py --config staging/load_config.yaml --tags story
cd driver && locust -f app.py --config staging/stress_config.yaml --tags story
cd driver && locust -f app.py --config staging/spike_config.yaml --tags story
cd driver && locust -f app.py --config staging/soak_config.yaml --tags story
```

#### Run all Stories by excluding unread notifications endpoint

```shell
cd driver && locust -f app.py --config staging/load_config.yaml --tags story --exclude-tags unread_notifications
cd driver && locust -f app.py --config staging/stress_config.yaml --tags story --exclude-tags unread_notifications
cd driver && locust -f app.py --config staging/spike_config.yaml --tags story --exclude-tags unread_notifications
cd driver && locust -f app.py --config staging/soak_config.yaml --tags story --exclude-tags unread_notifications
```


### Experiment results

Results of experiments are displayed in a table. 

Here's the table structure:

* `Type` is type of the API operation. E.g. GET, POST, PUT, etc.
* `Name` is the name of operation which is programmatically set by us through our code.
* `reqs` indicates number of total requests invoked by locust.
* `fails` indicates number of failure requests.
* `Avg` indicates the average response time (ms) is taken for a request to complete.
* `Min` indicates the minimum response time (ms) is taken for a request to complete.
* `Max` indicates the maximum response time (ms) is taken for a request to complete.
* `Med` indicates the median response time (ms) is taken for a request to complete.

And another table for response time percentiles as following:

* `Type` is type of the API operation. E.g. GET, POST, PUT, etc.
* `Name` is the name of operation which is programmatically set by us through our code.
* `50%` indicates response time (ms) is taken for 50th percentile of requests to complete.
* `66%` indicates response time (ms) is taken for 66th percentile of requests to complete.
* `75%` indicates response time (ms) is taken for 75th percentile of requests to complete.
* `80%` indicates response time (ms) is taken for 80th percentile of requests to complete.
* `90%` indicates response time (ms) is taken for 90th percentile of requests to complete.
* `95%` indicates response time (ms) is taken for 95th percentile of requests to complete.
* `99%` indicates response time (ms) is taken for 99th percentile of requests to complete.
* `100%` indicates response time (ms) is taken for 100th percentile of requests to complete.

### Outputs

In order to produce report in **html** file, use `--html` flag as shown below:

```shell
cd driver && locust -f app.py --config staging/load_config.yaml --html load_testing.html
cd driver && locust -f app.py --config staging/stress_config.yaml --html stress_testing.html
cd driver && locust -f app.py --config staging/spike_config.yaml --html spike_testing.html
cd driver && locust -f app.py --config staging/soak_config.yaml --html soak_testing.html
```
