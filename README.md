
# CSCE 689 -> TAMU, 2022 | ML Based Cyberdefenses - Competition #
## Description -> Machine Learning based AV - Binary Classification ##

Blog talking about the Competition [here](https://ml-to-cs.sidharthbaveja.com/competition/)

Results can be found [here](https://docs.google.com/spreadsheets/d/1Phf5sTbCE8c16iRW4brKIYG52AaRb2L2/edit?usp=sharing&ouid=106247587660774829285&rtpof=true&sd=true)

## Stages of the competition ##
  i. Defense
 ii. Attack

-> Defenders Challenge Specifications:

Deliverable: Self-contained docker image with model querying via HTTP requests.

Goals:

	 FPR: 1% | TPR: 95%

Constraints:

	 Memory: 1 GB max RAM
	 Response time: 5 seconds per sample
	 Warning: Timeouts will be considered evasions.

-> Attackers Challenge Specifications:

Deliverable: Evasive Malware Binaries.

Goals:

     Evade the most models possible.

Constraints:

	Maximum file size: 5MB of appended data.
	Evasive sample execution in sandbox must be equivlent to original sample.

Minimum score for grading:
	At least one sample must bypass at least one model.
