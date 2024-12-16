## GreenFaaS

The objective is to propose a FaaS (Function-as-a-Service) architecture that executes functions while consuming the least amount of energy possible, all while maintaining the expected quality of results for the user. To achieve this, we propose **GreenFaaS**, a solution in which a client can register multiple alternative implementations for a given function intended to perform a task. These alternatives may differ in terms of the algorithm used or the resources allocated for execution. Each implementation will complete the requested task but may produce results of varying quality while consuming different amounts of energy. The service provider, based on its energy budget and taking into account the user’s expectations, will determine and propose the alternative that consumes the least energy while producing a result of acceptable quality for the user.

To solidify the proposed idea, we will first develop the project's motivation by creating alternative implementations of a state-of-the-art benchmark. These alternatives will then be implemented and executed on Apache OpenWhisk, an open-source platform for cloud-based function deployment, while monitoring energy consumption, execution time, and the quality of results for each alternative.

## How to Run experiment ? 

1. Install and configure openwhisk
2. Install and configure OpenstackSwift
3. Run every benchmark experiment by follow the lead in each benchmark folder. 

## Some results
