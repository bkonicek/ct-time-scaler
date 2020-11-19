import os
from datetime import datetime
from dotenv import load_dotenv
from kubernetes import client, config

load_dotenv()

DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME')
NAMESPACE = os.getenv('NAMESPACE', 'default')


def getMinutesLastDigit():
    currTime = datetime.now()
    currMinutes = currTime.strftime("%M")
    currTime = currTime.strftime("%H:%M:%S")
    lastDigit = int(currMinutes[-1])
    return currTime, lastDigit


def main():
    config.load_kube_config()

    v1 = client.AppsV1Api()
    now, numReplicas = getMinutesLastDigit()
    repBody = {
        "spec": {
            "replicas": numReplicas}
    }
    print("Current time is %s. Scaling deployment %s to %d replicas" %
          (now, DEPLOYMENT_NAME, numReplicas))
    v1.patch_namespaced_deployment(
        name=DEPLOYMENT_NAME, namespace=NAMESPACE, body=repBody)


if __name__ == "__main__":
    main()
