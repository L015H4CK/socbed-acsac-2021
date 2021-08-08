# Reproducing our Experiments

## Overview

In our paper, we present SOCBED, which is an open-source testbed for reproducible log data generation.
The testbed is based on seven virtual machines (VMs) that can be automatically built by provisioning scripts.
In our evaluation, we performed ten iterations of a SOCBED simulation on two different host systems and with two different logging configurations, respectively, resulting in a total of 40 iterations.

In this document, we describe three levels to verify/reproduce our measurements.
The levels build on each other, starting with the least effort:

1. Recalculating the presented results from our dataset
2. Reproducing one type of simulation (one host and one logging configuration only)
3. Reproducing the full evaluation

Please note that a full reproduction of the evaluation (level three) is very time-consuming and requires two separate host systems:
Each iteration of our simulation takes around 70 minutes, resulting in around 24 hours of simulation time per host.
Building the VMs requires an additional 3-5 hours (depending on host and internet speed) and is required twice per host.
We therefore propose to limit the reproduction to level two and only run a few simulation iterations, whose results can then be compared to our dataset.
However, we provide all necessary instructions for a full reproduction in case this is feasible.

In the following, we describe how to perform the three levels of reproduction.

## Recalculating the presented results from our dataset

Our main results are presented in Table 2 (page 8) and Figure 5 (page 9) of the paper.
They are based on the measurements contained in `dataset.zip`.
Each directory in this archive contains all relevant log data from ten simulation runs, respectively.
For the reproduction of results, we only require the Sigma alerts (`sigma_##.jsonl`), Suricata alerts (`syslog_##.jsonl`), and the Windows Event logs (`winlogbeat_##.jsonl`).

### Recalculating Table 2

The means and standard deviations were calculated using the LibreOffice spreadsheet `True Positives.fods`.
You can find all values of Table 2 in columns AP-AW of the tab "Iterations Used for Evaluation".

All measurements for the 40 iterations (columns B-AO) can be recalculated from the dataset using Python 3 scripts.
To recalculate the number of Sigma alerts (line 8-12) execute the following command in a shell (such as Bash):

```sh
find dataset -name 'sigma_??.jsonl' -exec python3 count_tps_sigma.py {} \;
```

For the Suricata alerts, execute

```sh
find dataset -name 'syslog_??.jsonl' -exec python3 count_tps_suricata.py {} \;
```

Please note that due to the alphabetical search order of `find`, "default" and "best practice" results are switched as compared to the spreadsheet.

### Recalculating Figure 5

Figure 5 is calculated from the Windows Event logs in the dataset (`winlogbeat_##.jsonl`).
We recommend creating a Python virtual environment and running the plot script within:

```sh
python3 -m venv venv
source venv/bin/activate
pip install matplotlib pandas seaborn
python3 boxplot.py dataset/
deactivate
```

## Reproducing one type of simulation

For our evaluation, we built and run SOCBED on two separate host systems with two different logging configurations (default and best-practice), respectively.
To begin with, this section describes how to build and run SOCBED on one host with the best-practice configuration.

### Building SOCBED

The setup process is described in the file `README.md` in the repository root.
Please build SOCBED by closely following these instructions and run the tests as described to verify correct functionality.

Attention: SOCBED requires a Windows 10 ISO image, as described in the readme file.
For the evaluation, we used Windows 10 Pro version 2004 (Build 19041).
We did not test later versions and therefore recommend to use exactly this version.
You can use the following image, which we uploaded to Google Drive: https://drive.google.com/file/d/1IoSszrbUf3b3od3rtba_fpoE5iZQKYkP/view?usp=sharing.

### Running an iteration of our simulation

After installing SOCBED successfully, you can run an iteration of our simulation as follows:

```sh
cd evaluation
source ~/.virtualenvs/socbed/bin/activate
pip install elasticsearch elasticsearch-dsl
./run_simulations
```

The simulation will take approx. 70 minutes.
During the simulation and at the end, several log files will be created (in the same directory), including the Windows Event logs and Linux syslogs downloaded from the VMs.
Sigma and Suricata alerts can be extracted from these files as shown in the previous section ("Recalculating the presented results from our dataset").

## Reproducing the full evaluation

The previous section described how to perform one iteration of the simulation on one host.
Our full evaluation differs from this description in the following aspects:

1. We performed 10 iterations of each configuration on each host instead of one. To change the number of iterations, open `run_simulations` and set `NUM_ITERATIONS=10` (line 3). Make sure to move/backup any old simulation output files before starting a new simulation because they will be overwritten.
1. We repeated the iterations with a changed Windows logging configuration. To do so, open `provisioning/ansible/client10_playbook.yml` and remove the roles `win10_logging_config` and `win10_sysmon`. This will change from the "best practice" to the "default" logging configuration. Then delete the client VM from VirtualBox and rebuilt it using the script `tools/build_client`.
1. We repeated the whole process (i.e., ten iterations per configuration) on another host.

Following these steps and then performing the calculations described in the section "Recalculating the presented results from our dataset" reproduces our complete evaluation.