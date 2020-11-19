import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
from kubernetes import client, config

load_dotenv()

DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME')
if DEPLOYMENT_NAME == None:
    print("You must provide a deployment name.")
    sys.exit(1)
NAMESPACE = os.getenv('NAMESPACE', 'default')
INTERVAL = int(os.getenv('UPDATE_INTERVAL', '60'))


def getMinutesLastDigit():
    currTime = datetime.now()
    currMinutes = currTime.strftime("%M")
    currTime = currTime.strftime("%H:%M:%S")
    lastDigit = int(currMinutes[-1])
    return currTime, lastDigit


def main():
    try:
        config.load_incluster_config()
    except:
        print("application is not running in a Pod, using local config")
        config.load_kube_config()

    v1 = client.AppsV1Api()
    while True:
        now, numReplicas = getMinutesLastDigit()
        repBody = {
            "spec": {
                "replicas": numReplicas}
        }
        status = v1.read_namespaced_deployment_status(
            name=DEPLOYMENT_NAME, namespace=NAMESPACE)
        if status.spec.replicas == numReplicas:
            print("Correct number of replicas already running")
        else:
            print("Current time is %s. Scaling deployment %s to %d replicas" %
                  (now, DEPLOYMENT_NAME, numReplicas))
            v1.patch_namespaced_deployment(
                name=DEPLOYMENT_NAME, namespace=NAMESPACE, body=repBody)
        print("Running again in %d seconds" % INTERVAL)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
