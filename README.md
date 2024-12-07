## GreenFaaS

The goal is to design a FaaS architecture that minimizes energy consumption while meeting user expectations for result quality. We propose **GreenFaaS**, where clients can register multiple alternative implementations of a function, differing in algorithms or resource usage. The service provider, considering its energy budget and user expectations, selects the most energy-efficient alternative that delivers acceptable quality.

To solidify the proposed idea, we will first develop the project's motivation by creating alternative implementations of a state-of-the-art benchmark. These alternatives will then be implemented and executed on Apache OpenWhisk, an open-source platform for cloud-based function deployment, while monitoring energy consumption, execution time, and the quality of results for each alternative.

## How to Run ? 

1. Install openwhisk
2. Install OpenstackSwift
3. Run every benchmark experiment by follow the lead in each read me for each benchmark. 