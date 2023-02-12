## How to create new test cases ?
Please refer to ```environments/``` and ```tasksall/```. Find more locust documentations in https://locust.io/

## Running Locust docker locally (standalone mode)

**Warning** latest tag is not compatible with the helm charts.

```bash
./scripts/local_start.sh <target_host> <test_script> <task_root optional>
```
**Example**
```bash
./scripts/local_start.sh host.docker.internal:8080 poseidon/test_extension-service
```

```bash
./scripts/local_start.sh host.docker.internal:8080 test_entry tasks/orca-search-service
```

### Accessing Locust standalone UI
Visit http://localhost:8089/


## Running Locust on k8s (master-slave mode)
If you want to run a heavy-loading test, your standalone localhost will be the bottleneck of generating heavy traffic. By running distributed locust on k8s, you can offload the loading onto k8s nodes and generate the traffic as much as you want.

**NOTE-1**: Locust will be deployed in DEV env, it only can access the endpoint in the same dev vpc, if it is not exposed to internet.

**NOTE-2**: Locust will be deployed in ```locust``` namespace of development cluster. If you are using locust to test services located in another namespace, follow the format to change the hostname ```<servicename>.<namespace>.svc.cluster.local```  [reference](https://stackoverflow.com/questions/37221483/service-located-in-another-namespace).

**NOTE-3**: Developers have full permission to  deploy apps to locust namespace on k8s. Please remember to remove created pods manually after task completion.

**NOTE-4**: In order to prevent `data: Too long: must have at most 1048576 bytes` error when running `./install.sh`, each team should put task files into a dedicated folder in tasksall. Testing files that are directly put into `tasksall` will be ingored by `./install.sh`. The install script will copy all testing files under `tasksall/<team folder>` to `task` folder and only pack files in `task` folder into locust helm chart.
```
/tasksall
 - /mermaid
  - test1.py
 - /poseidon
  - test2.py
 ...
```

### Deploying Locust on K8s
- Requires helm v3 or above.

#### Deploy Locust to specified namespace

```bash
./install.sh environments/<test_case>.yaml tasksall/<team folder> <release_name> <namespace>
```

For example:
```bash
./install.sh environments/test_mermaid.yaml tasksall/mermaid mermaid-howard-locust sb-dep-dev-team-hermes
```

### Access locust UI
- Make sure you've installed [kubectl](https://shopadmin.atlassian.net/wiki/spaces/SE/pages/424214706/Installation).
```
./forward.sh
```

#### Access locust UI with specified namespace
```
./forward.sh <namespace>
```
For example
```bash
./forward.sh sb-dep-dev-team-poseidon
```

Visit http://localhost:8089/

### Remove locust
```bash
./remove.sh
```
#### Remove from specified namespace
```bash
./remove.sh <namespace>
```
For example
```bash
./remove.sh sb-dep-dev-team-poseidon
```

(content below is from https://github.com/helm/charts/tree/master/stable/locust)


## Locust Helm Chart

This is a templated deployment of [Locust](http://locust.io) for Distributed Load
testing using Kubernetes.

## Pre Requisites:

* Requires (and tested with) helm `v2.1.2` or above.

## Chart details

This chart will do the following:

* Convert all files in `tasks/` folder into a configmap
* If an existing configmap is specified, it will be used instead of building one from the chart
* Create a Locust master and Locust worker deployment with the Target host
  and Tasks file specified.


### Installing the chart

To install the chart with the release name `locust-nymph` in the default namespace:

```bash
helm install -n locust-nymph --set master.config.target-host=http://site.example.com stable/locust
```

| Parameter                    | Description                             | Default                                               |
| ---------------------------- | ----------------------------------      | ----------------------------------------------------- |
| `Name`                       | Locust master name                      | `locust`                                              |
| `image.repository`           | Locust container image name             | `peterevans/locust`                                  |
| `image.tag`                  | Locust Container image tag              | `0.9.0`                                               |
| `image.pullSecrets`          | Locust Container image registry secret  | `None`                                                |
| `service.type`               | k8s service type exposing master        | `NodePort`                                            |
| `service.nodePort`           | Port on cluster to expose master        | `0`                                                   |
| `service.annotations`        | KV containing custom annotations        | `{}`                                                  |
| `service.extraLabels`        | KV containing extra labels              | `{}`                                                  |
| `extraVolumes`               | List of extra Volumes                   | `[]`                                                  |
| `extraVolumeMounts`          | List of extra Volume Mounts             | `[]`                                                  |
| `extraEnvs`                  | List of extra Environment Variables     | `[]`                                                  |
| `master.config.target-host`  | locust target host                      | `http://site.example.com`                             |
| `master.nodeSelector`        | k8s nodeselector                        | `{}`                                                  |
| `master.tolerations`         | k8s tolerance                           | `{}`                                                  |
| `worker.config.locust-script`| locust script to run                    | `/locust-tasks/tasks.py`                              |
| `worker.config.configmapName`| configmap to mount locust scripts from  | `empty, configmap is created from tasks folder in Chart` |
| `worker.replicaCount`        | Number of workers to run                | `2`                                                   |
| `worker.nodeSelector`        | k8s nodeselector                        | `{}`                                                  |
| `worker.tolerations`         | k8s tolerance                           | `{}`                                                  |

Specify parameters using `--set key=value[,key=value]` argument to `helm install`

Alternatively a YAML file that specifies the values for the parameters can be provided like this:

```bash
$ helm install --name my-release -f values.yaml stable/locust
```

#### Creating configmap with your Locust task files

You're probably developing your own Locust scripts that you want to run in this distributed setup.
To get those scripts into this deployment you can fork the chart and put them into the `tasks` folder. From there
they will be converted to a configmap and mounted for use in Locust.

Another solution, if you don't want to fork the Chart, is to put your Locust scripts in a configmap and provide the name
as a config parameter in `values.yaml`. You can read more on the use of configmaps as volumes in pods [here](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/).

If you have your Locust task files in a folder named "scripts" you would use something like the following command:

`kubectl create configmap locust-worker-configs --from-file path/to/scripts`


### Interacting with Locust

Get the Locust URL following the Post Installation notes. Using port forwarding you should be able to connect to the
web ui on Locust master node.

You can start the swarm from the command line using port forwarding as follows:

for example:
```bash
export LOCUST_URL=http://127.0.0.1:8089
```

Start / Monitor & Stop the Locust swarm via the web panel or with following commands:

Start:
```bash
curl -XPOST $LOCUST_URL/swarm -d"locust_count=100&hatch_rate=10"
```

Monitor:
```bash
watch -n 1 "curl -s $LOCUST_URL/stats/requests | jq -r '[.user_count, .total_rps, .state] | @tsv'"
```

Stop:
```bash
curl $LOCUST_URL/stop
```
