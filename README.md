# CT-Time-Scaler
A time-based autoscaler written in Python as a proof of concept.

## Description
The scaler app checks the current time and uses the Kubernetes API to scale up
or down the given deployment based on the value of the last digit of the current time.

For example, at 03:5**2** it should scale the deployment to **2** replicas. At 03:5**3** it should scale it up to 3 replicas. At 04:00 it should scale down to 0 running replicas.

If run locally it uses the current context of the workstation's `~/.kube/config` file. If run within a pod it uses a service account to configure the API client.

## Usage
Run the application locally or deploy with the provided helm chart to
scale up or down a deployment based on the last digit of the minutes value
of the current time.

## Installation
Update the provided `values.yaml` with your desired settings

| Key | Description | Required? |
|-----|-------------|-----------|
| image.repository | name of the Docker image | x |
| image.tag | version of the image to use | x |
| image.pullPolicy | PullPolicy for the image | x |
| replicaCount | Number of replicas to run | x |
| deployName | Name of the deployment you want to scale | x |
| checkInterval | How often to update replica count (default: 60 seconds) | |

If running locally create an `.env` file in the root of the directory with values
set for `DEPLOYMENT_NAME`, `NAMESPACE`, and (optionally) `UPDATE_INTERVAL`.

If using Helm, run `helm install -f values.yaml ct-scaler .` in the same namespace as the deployment you want it to scale. 

Once it's installed you should see the other deployment's replica count has changed, unless the current time happens to match the current number of replicas.

You can verify it's working by running `kubectl logs` on the time-scaler pod. The output should look something like
```
Current time is 16:54:35. Scaling deployment nginx-nginx to 4 replicas
Running again in 60 seconds
```
