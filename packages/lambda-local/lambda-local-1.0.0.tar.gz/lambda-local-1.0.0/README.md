# LAMBDA LOCAL 

Running a AWS lambda function in local host or pycharm. 
Here we can run and debug the AWS lambda function from pycharm. 


### Lambda handler function 

```
def handler(events, context):
    print("events :", events)
    print("context :", context)
    return events
```

### Local lambda run 
```
from lambda_local.lambda_local import LambdaLocal

events = {"x": 7}

context = {"timeout": 100}

LambdaLocal(handler, events, context).run()

```
