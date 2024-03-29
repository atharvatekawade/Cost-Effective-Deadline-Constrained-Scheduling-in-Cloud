# Cost-Effective-Deadline-Constrained-Scheduling-in-Cloud

This problem is of scheduling applications modeled as a directed acyclic graph in a cost-effective way subject to a given deadline in a multi-cloud system. The model
includes the billing mechanisms and costs for transferring data across clouds for different cloud providers. Our proposed methodology is compared with the following state-of-art algorithms:
1) (PSO) Deadline Based Resource Provisioning and Scheduling Algorithm for Scientific Workflows on Clouds - Maria Alejandra Rodriguez; Rajkumar Buyya: https://ieeexplore.ieee.org/document/6782394
2) (ADPSOGA) Cost-Driven Scheduling for Deadline-Based Workflow Across Multiple Clouds - Wenzhong Guo
Fujian Collaborative Innovation Center for Big Data Applications in Governments, Fuzhou University, Fuzhou, China
; Bing Lin; Guolong Chen; Yuzhong Chen; Feng Liang: https://ieeexplore.ieee.org/document/8476198

## Usage
Clone the repositary and run the command: python main.py -num -itr -aws -ma -gcp -D -smin -smax, the arguments are explained below:
1) ff: Represents the path of file which stores task graph in xml format.
2) itr: Represents the number of iterations to run the algorithms, with average results reported at the end.
3) aws: Represents the number of cloud providers following AWS pricing.
4) ma: Represents the number of cloud providers following Microsoft Azure pricing.
5) gcp: Represents the number of cloud providers following GCP pricing.
6) smin: Represents the lower bound for task computation requirement and edge data.
7) smax: Represents the upper bound for task computation requirement and edge data.

Upon running the command and successful execution, we get plots for the cost and makespan of different algorithms. The makespan plot also includes the deadline for reference. Sample plots are shown below.

## Results
![Figure_1](https://user-images.githubusercontent.com/64606981/206895608-d4b76f19-6ae4-4c7f-b497-d2e6b1459dc2.png)
