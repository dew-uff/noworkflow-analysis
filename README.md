# Evaluation

This is an experiment made to show how noWorkflow's features can help scientists working on in virtuo and in silico experiments.

The experiment is a machine learning experiment to find fraud in credit cards. Its (code)[/credit_card_fraud.py] is in this repository but the the file 'creditcard.csv' used in the code is the [Kaggle Credit Card Fraud Detection Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud). Furthermore, note that there is an unnecessary loop when initializing the object \textbf{RandomUnderSampler}. We wrote the code like this to help us show some of noWorkflow's features.

Other than that, we ran the experiment twice, meaning we did two trials of the same experiment. The difference between the two trials is the value of the seed, the variable \textbf{random\_seed}. On the first trial, we used the value 42, and in the second trial, we used the value 40, passing it as a script parameter.

The steps we took in this simulation are listed below:

1. now run credit_card_fraud.py
2. now run credit_card_fraud.py 42

## Materials and Methods

Despite the fact that our experiment was successful when simulating a collaborative environment, we need a way to judge if the provenance collected meets the researchers' needs. So, we decided to use the [First Provenance Challenge](https://openprovenance.org/provenance-challenge/FirstProvenanceChallenge.html) and its questions to see if noWorkflow's collected provenance is useful even if we are in a collaborative environment.

However, there are two problems with using the First Provenance Challenge and its questions directly. The first one is that the challenge is about a specific workflow that is different from ours. The second one is that the questions are about that workflow. The key word being 'workflow', because it's not a script like our experiment. Therefore, we decided to adapt the questions in the First Provenance Challenge to include scripts in general.

Before adapting the First Provenance Challenge's questions to scripts, we propose some notations to differentiate between the aspects of a script. They are:

<!-- - T is the set of all trials in a experiment
- s is a script
- F is the set of all functions in a script(s)
- f is one funtion of F (f∈F)
- PF is the set of all parameters in all functions(F) in a script(s)
- pf is one parameter of PF (pf∈PF)
- P is the set of all parameters a script(s) receives when it's called
- p is one parameter of P(p∈P)
- OS is the set of all outputs of a script(s)
- os one output of OS
- OSF is the set of all outputs(return) of a function of a script
- osf is one output(return) of OSF
- d is a date
- a is an annotation
- ac is an annotation(a) content -->

- An experiment e, materialized in the form of a script s is composed of a set of trials T
- Each trial t∈T corresponds to a different execution of the script s.
- The set of trials T of an experiment may correspond to executions of different versions of the script s, including variations of code, parameters, and inputs.
- A trial t may have zero or more parameters p (these are the parameters that are passed in the command line during the invocation of the script s).
- P is the set of all parameters of a trial t (p∈P ).
- A trial t may generate zero or more outputs os. We call OS the set of all such outputs (os∈OS). We consider an output to be a file that is written by the script.
- A trial t has a (possibly empty) set of functions F . A function f of a trial thus belongs to this set (f∈F).
- The functions of a trial t may have zero or more parameters.
- We call PF the set of all parameters of the functions in F of t. We call pf a given parameter of P F (pf∈PF).
- A function f of t may produce a set of outputs (generated via the return statement) OSF , where osf is one of such outputs (osf∈OSF).

|Query number|First Provenance Challenge Query|Query change to general script|
| -------- | ------- | -------- |
|1|Find the process that led to Atlas X Graphic / everything that caused Atlas X Graphic to be as it is. This should tell us the new brain images from which the averaged atlas was generated, the warping performed etc.|Given an output os of a trial t, get all the functions F', (F'⊆F ) that generated or changed os.|
|2|Find the process that led to Atlas X Graphic, excluding everything prior to the averaging of images with softmean.|Given an output os of a trial t, get all the functions F', (F'∈F) that generated or changed os, excluding everything prior to a function f, (f∈F and f∈F')|
|3|Find the Stage 3, 4 and 5 details of the process that led to Atlas X Graphic.|---------|
|4|Find all invocations of procedure align_warp using a twelfth order nonlinear 1365 parameter model (see model menu describing possible values of parameter "-m 12" of align_warp) that ran on a Monday.|Given a function f, get all calls of f that had pf as a parameter and were executed on the date d.|
|5|Find all Atlas Graphic images outputted from workflows where at least one of the input Anatomy Headers had an entry global maximum=4095. The contents of a header file can be extracted as text using the scanheader AIR utility.|Get all the outputs OS of all trials in T that had a parameter p as an input.|
|6|Find all output averaged images of softmean (average) procedures, where the warped images taken as input were align_warped using a twelfth order nonlinear 1365 parameter model, i.e. "where softmean was preceded in the workflow, directly or indirectly, by an align_warp procedure with argument -m 12."|Find all outputs (produced by the return statement) of a function f,(f∈F) if f is preceded by f', (f'∈F) and f' received the parameter pf.|
|7|A user has run the workflow twice, in the second instance replacing each procedures (convert) in the final stage with two procedures: pgmtoppm, then pnmtojpeg. Find the differences between the two workflow runs. The exact level of detail in the difference that is detected by a system is up to each participant.|Given two trials t and t' contemplating the same experiment, find the difference between t and t' executions and functions.|
|8|A user has annotated some anatomy images with a key-value pair center=UChicago. Find the outputs of align_warp where the inputs are annotated with center=UChicago.|Find all outputs (produced by the return statement) of a function f, where f received a parameter pf and pf was annotated with a specific annotation a.|
|9|A user has annotated some atlas graphics with key-value pair where the key is studyModality. Find all the graphical atlas sets that have metadata annotation studyModality with values speech, visual or audio, and return all other annotations to these files.|Find all the outputs OS of all trials in T where the outputs were annotated with a specific content ac. For those outputs, return all their other annotations.|

Notice that we didn't adapt the Query number 3 to contemplate scripts. We didn't because Query number 3 specifies Stages exclusive to the First Provenance Challenge's workflow. We could arbitrarily separate the script used in our experiment into stages, but that would make the new query not include scripts in general but just ours.


## Results

Now that we have the First Provenance Challenge Queries adapted to script, we can use noWorkflow's collected provenance and features to answer them.

### 1 - Given an output os of a trial t, get all the functions F', (F'⊆F ) that generated or changed os.

dataflow + wdf

### 2 - Given an output os of a trial t, get all the functions F', (F'∈F) that generated or changed os, excluding everything prior to a function f, (f∈F and f∈F').

dataflow + wdf -> click on the last function -> ctrl+click on f

### 4 - Given a function f, get all calls of f that had pf as a parameter and were executed on the date d.

To answer this query, we first must select the date d. We chose 08/25/2025 at 3 p.m. We also must select a parameter and a function; we went with the parameter "0.2" and the function "train_test_split".

So, we want to find all calls of "train_test_split" with the parameter "0.2" that were executed in "08/25/2025 at 3 p.m". For that, we can use a SQL query. First, we must query the table evaluation to get "0.2" as an evaluation, then we must check which evaluations depend on it. After getting its code_component id, we get the code_component name (how the function is called in the code) and finally query all its calls with a join with the table trial so we can specify the date.
```
SELECT *
FROM code_component as c
LEFT JOIN trial as t on c.trial_id == t.id
LEFT JOIN tag as ta on ta.trial_id == t.id
WHERE t.start LIKE "2025-08-25 15%" AND c.name == (
	SELECT c.name
	FROM code_component as c
	WHERE c.id IN 
	(SELECT e1.code_component_id
		FROM evaluation as e1
		WHERE e1.id IN 
			(SELECT d.dependent_id
			FROM dependency as d
			WHERE d.dependency_id IN 
				(SELECT e.id
				FROM evaluation as e
				WHERE e.repr == '0.2' AND d.type == "argument") 
	AND name LIKE "%train_test_split%")
```

### 5 - Get all the outputs OS of all trials in T that had a parameter p as an input.

Before answering this query, we must decide the value of the parameter first. In our experiment, only one trial had a parameter passed to it when its scripts were called. The parameter is "42".

A SQL query in three tables can answer our Query number 5. We need to query the table file_access to get the outputs, because it's the table that registers the access to files, including writing, meaning the outputs from a trial. We also need to query the table activation. This table registers function calls. We must make sure that the file accesses we are querying are the right ones. The table argument must be checked too. After all, this is the table responsible for checking if the trial received a parameter when it was executed and which parameter it is. 

```
SELECT *
FROM file_access as f, activation as ac, argument as ar
LEFT JOIN tag as ta on ta.trial id == f.trial id
WHERE ac.id == f.activation id AND
ar.trial id == f.trial id
AND f.trial_id == ac.trial id
AND (f.mode == "w" OR f.mode == "w+b")
AND f.name NOT LIKE "nul"
AND ar.name == "argv"
AND ar.value LIKE "%’40’%"
```

6 - Find all outputs (produced by the return statement) of a function f,(f∈F) if f is preceded by f', (f'∈F) and f' received the parameter pf.
<!-- [Script without noWorkflow](/provenance_challenge_5_no_noworkflow.py) -->

[Script with noWorfkflow](/provenance_challenge_5_with_noworkflow.py)

### 7 - Given two trials t and t' contemplating the same experiment, find the difference between t and t' executions and functions.

click on t->shift+click on t'

### 8 - Find all outputs (produced by the return statement) of a function f, where f received a parameter pf and pf was annotated with a specific annotation a.

This is a query that presently noWorkflow can't answer. It doesn't have the feature to put annotations in files, nor does it support it. Meaning it can't know if a parameter of a function was annontated (or not), nor can it annotate it.

### 9 - Find all the outputs OS of all trials in T where the outputs were annotated with a specific content ac. For those outputs, return all their other annotations.

This is a query that presently noWorkflow can't answer. It doesn't have the feature to put annotations in files, nor does it support it. Meaning it can't know if a parameter of a function was annontated (or not), can't annotate it, nor can read the annotation's content.
