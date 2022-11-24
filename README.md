# Cost-Effective-Deadline-Constrained-Scheduling-in-Cloud

This problem is of scheduling applications modeled as a directed acyclic graph in a cost-effective way subject to a given deadline in a multi-cloud system. The model
includes the billing mechanisms and costs for transferring data across clouds for different cloud providers. Our proposed methodology is compared with the following state-of-art algorithms:
1) Deadline Based Resource Provisioningand Scheduling Algorithm for Scientific Workflows on Clouds - Maria Alejandra Rodriguez; Rajkumar Buyya: https://ieeexplore.ieee.org/document/6782394
2) Cost-Driven Scheduling for Deadline-Based Workflow Across Multiple Clouds - Wenzhong Guo
Fujian Collaborative Innovation Center for Big Data Applications in Governments, Fuzhou University, Fuzhou, China
; Bing Lin; Guolong Chen; Yuzhong Chen; Feng Liang: https://ieeexplore.ieee.org/document/8476198

## Usage
Clone the repositary and run the command: python main.py -num -itr -p -D -smin -smax, the arguments are explained below:
1) num: Represents the number of nodes of an Epigenomics task graph.
2) itr: Represents the number of iterations to run the algorithms, with average results reported at the end.
3) p: Represents the number of cloud providers, which should be a multiple of 3: p/3 for Microsoft Azure, p/3 for AWS and p/3 for GCP type clouds.
4) D: Represents the deadline constraint as a factor w.r.t makespan obtained using the HEFT algorithm.
5) smin: Represents the lower bound for task computation requirement and edge data.
6) smax: Represents the upper bound for task computation requirement and edge data.

## Results
![Figure_1](https://user-images.githubusercontent.com/64606981/203848744-0569fb98-5718-462e-9841-e7f5cb38696f.png)
