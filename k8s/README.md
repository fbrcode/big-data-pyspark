# Spark Install (Option #2)

Sequence of commands using ubuntu jammy LTS release.

## Install Java JRE

```sh
apt update
apt install default-jre -y
java -version
```

## Install and Setup Spark

```sh
# download & unzip spark from the archives: https://archive.apache.org/dist/spark/
wget https://archive.apache.org/dist/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz
tar -xzf spark-3.3.0-bin-hadoop3.tgz

# copy to /opt standard apps directory
sudo mv spark-3.3.0-bin-hadoop3 /opt/spark

# add environment variables to run spark
echo -en "\n# spark environment variables setup\n" >> ~/.bashrc
echo -en "export SPARK_HOME=/opt/spark\n" >> ~/.bashrc
echo -en "export PATH=\$PATH:\$SPARK_HOME/bin:\$SPARK_HOME/sbin\n" >> ~/.bashrc
source ~/.bashrc
```

Test it out by connecting to spark **scala shell** option (CTRL+D to quit) by typing `spark-shell`

Test it out by connecting to spark **python shell** option (CTRL+D to quit) by typing `pyspark`

## Install additional python libraries in virtual environment (venv)

Standard sequence to install and use python virtual environment:

- Check existing python install: `apt list python3 -a`
- Install pip module (as root): `apt install python3-pip -y`
- Install virtual environment module (as root): `apt install python3-venv -y`
- Create a virtual environment: `python3 -m venv env`
- Add `.gitignore` with the line `env` to skip it on SCM
- Start virtual environment: `source env/bin/activate`
- List existing modules in the virtual environment: `pip list -v`
- Stop virtual environment: `deactivate`

### Install python libraries for spark project

```sh
source env/bin/activate
pip install numpy
pip install pandas
pip list -v
```

## Docker install

```sh
# run as root
apt update
apt upgrade -y
# install dependencies
apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y
# add docker’s official GPG key
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/trusted.gpg.d/docker-archive-keyring.gpg
# setup docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
# install docker engine
apt update
apt install docker-ce docker-ce-cli containerd.io -y
docker --version
# add user 'vm' to run docker commands
usermod -aG docker vm
newgrp docker
systemctl restart docker
systemctl enable docker
systemctl status docker
# as 'vm' user, run web server locally and map to local to access in browser
docker run --name testnginx -p 80:80 -d nginx
ssh -L 8090:localhost:80 vm@vm # on another terminal
# access the url http://localhost:8090/
```

## Kubernetes install

Minikube is a lightweight implementation of k8s for local executions.

Reference: <https://minikube.sigs.k8s.io/docs/start/>

```sh
# get minikube and install (arm64 arch)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-arm64
sudo install minikube-linux-arm64 /usr/local/bin/minikube
```

Kubectl is a command line tool to interact with kubernetes (k8s)

Reference: <https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/>

```sh
# get kubectl and install (arm64 arch)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client --output=yaml
```

Starting local kubernetes and interacting

```sh
# start kubernetes
minikube start
```

Output:

```txt
😄  minikube v1.27.1 on Ubuntu 22.04 (arm64)
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.25.2 on Docker 20.10.18 ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

Check status

```sh
minikube status

# minikube
# type: Control Plane --> only one node
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured
```

Getting cluster information:

```sh
kubectl cluster-info
# Kubernetes control plane is running at https://192.168.49.2:8443
# CoreDNS is running at https://192.168.49.2:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

To check the environment:

```sh
kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   36h
```

## Running kubernetes modes

- Imperative: `kubectl run ...` - used for experiments, i.e.: `kubectl run nginx --image nginx`
- Declarative: `kubectl apply ...` - used for script executions in YAML/JSON, i.e.: `kubectl apply -f new_pod.yaml`

## Kubernetes imperative example

```sh
# run nginx pod image (imperative)
kubectl run pod-nginx --image nginx

# check status
kubectl get all
# NAME            READY   STATUS    RESTARTS   AGE
# pod/pod-nginx   1/1     Running   0          56s

kubectl get pods
# NAME        READY   STATUS    RESTARTS   AGE
# pod-nginx   1/1     Running   0          67s

kubectl get nodes
# NAME       STATUS   ROLES           AGE   VERSION
# minikube   Ready    control-plane   36h   v1.25.2

kubectl describe pods
# Name:             pod-nginx
# Namespace:        default
# Priority:         0
# Service Account:  default
# Node:             minikube/192.168.49.2
# Start Time:       Fri, 21 Oct 2022 10:39:52 +0000
# Labels:           run=pod-nginx
# Annotations:      <none>
# Status:           Running
# IP:               172.17.0.3
# IPs:
#   IP:  172.17.0.3
# Containers:
#   pod-nginx:
#     Container ID:   docker://d36545efe88e9d0e2990d44a9439b339d1e55b207493cc30882bf5640b5a23c9
#     Image:          nginx
#     Image ID:       docker-pullable://nginx@sha256:5ffb682b98b0362b66754387e86b0cd31a5cb7123e49e7f6f6617690900d20b2
#     Port:           <none>
#     Host Port:      <none>
#     State:          Running
#       Started:      Fri, 21 Oct 2022 10:40:19 +0000
#     Ready:          True
#     Restart Count:  0
#     Environment:    <none>
#     Mounts:
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-xpm5c (ro)
# Conditions:
#   Type              Status
#   Initialized       True
#   Ready             True
#   ContainersReady   True
#   PodScheduled      True
# Volumes:
#   kube-api-access-xpm5c:
#     Type:                    Projected (a volume that contains injected data from multiple sources)
#     TokenExpirationSeconds:  3607
#     ConfigMapName:           kube-root-ca.crt
#     ConfigMapOptional:       <nil>
#     DownwardAPI:             true
# QoS Class:                   BestEffort
# Node-Selectors:              <none>
# Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
#                              node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
# Events:
#   Type    Reason     Age   From               Message
#   ----    ------     ----  ----               -------
#   Normal  Scheduled  106s  default-scheduler  Successfully assigned default/pod-nginx to minikube
#   Normal  Pulling    106s  kubelet            Pulling image "nginx"
#   Normal  Pulled     80s   kubelet            Successfully pulled image "nginx" in 26.013508679s
#   Normal  Created    80s   kubelet            Created container pod-nginx
#   Normal  Started    79s   kubelet            Started container pod-nginx

# delete nginx pod
kubectl delete pod pod-nginx
```

## Kubernetes declarative example

```sh
# run nginx pod image (declarative)
kubectl apply -f pod-nginx.yaml

kubectl get pods
# NAME        READY   STATUS    RESTARTS   AGE
# pod-nginx   1/1     Running   0          8s

kubectl get all
# NAME            READY   STATUS    RESTARTS   AGE
# pod/pod-nginx   1/1     Running   0          27s

kubectl describe pods
# Name:             pod-nginx
# Namespace:        default
# Priority:         0
# Service Account:  default
# Node:             minikube/192.168.49.2
# Start Time:       Fri, 21 Oct 2022 16:05:33 +0000
# Labels:           <none>
# Annotations:      <none>
# Status:           Running
# IP:               172.17.0.3
# IPs:
#   IP:  172.17.0.3
# Containers:
#   nginx-container:
#     Container ID:   docker://9385169fdbb4c834c3dfdffee94af965e643a29e1e68fd3adbcd5063be8c23f6
#     Image:          nginx
#     Image ID:       docker-pullable://nginx@sha256:5ffb682b98b0362b66754387e86b0cd31a5cb7123e49e7f6f6617690900d20b2
#     Port:           80/TCP
#     Host Port:      0/TCP
#     State:          Running
#       Started:      Fri, 21 Oct 2022 16:05:36 +0000
#     Ready:          True
#     Restart Count:  0
#     Limits:
#       cpu:     500m
#       memory:  128Mi
#     Requests:
#       cpu:        500m
#       memory:     128Mi
#     Environment:  <none>
#     Mounts:
#       /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-5x74c (ro)
# Conditions:
#   Type              Status
#   Initialized       True
#   Ready             True
#   ContainersReady   True
#   PodScheduled      True
# Volumes:
#   kube-api-access-5x74c:
#     Type:                    Projected (a volume that contains injected data from multiple sources)
#     TokenExpirationSeconds:  3607
#     ConfigMapName:           kube-root-ca.crt
#     ConfigMapOptional:       <nil>
#     DownwardAPI:             true
# QoS Class:                   Guaranteed
# Node-Selectors:              <none>
# Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
#                              node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
# Events:                      <none>
```

## Interacting with container pod

Attaching to the existing running container

```sh
kubectl exec -it pod-nginx -- sh
```

## Using ReplicaSet for application management

ReplicaSet uses a selector to identify the pods/containers it has to maintain by using labels as identifiers.

It scales the number of pods according to the need.

```sh
# create a new replica set
kubectl apply -f replicaSet1.yaml
kubectl create -f replicaSet1.yaml

# scale an existing replica set
kubectl scale replicaSet redis-replicaSet --replicas=10
```

Running a example:

```sh
# create replica set for redis
kubectl apply -f redis-replicaSet.yaml

# check running pods
kubectl get all
# NAME                          READY   STATUS    RESTARTS   AGE
# pod/redis-replica-set-2dprl   1/1     Running   0          2m2s
# pod/redis-replica-set-mvjhp   1/1     Running   0          2m2s
# pod/redis-replica-set-s4qsx   1/1     Running   0          2m2s
#
# NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3d5h
#
# NAME                                DESIRED   CURRENT   READY   AGE
# replicaset.apps/redis-replica-set   3         3         3       2m2s

# scale to 6 replicas
kubectl scale replicaSet redis-replica-set --replicas=6

# check running pod again
kubectl get all
# NAME                          READY   STATUS    RESTARTS   AGE
# pod/redis-replica-set-2dprl   1/1     Running   0          5m40s
# pod/redis-replica-set-c7jzm   1/1     Running   0          22s
# pod/redis-replica-set-dsxfz   1/1     Running   0          22s
# pod/redis-replica-set-mzt2q   1/1     Running   0          106s
# pod/redis-replica-set-qvm4v   1/1     Running   0          22s
# pod/redis-replica-set-s4qsx   1/1     Running   0          5m40s
#
# NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3d5h
#
# NAME                                DESIRED   CURRENT   READY   AGE
# replicaset.apps/redis-replica-set   6         6         6       5m40s

# to terminate the replica set
kubectl delete replicaSet redis-replica-set
# replicaset.apps "redis-replica-set" deleted
```

## Using Deployment for ReplicaSet management

Deployment is a level above ReplicaSets and allows declarative updates to the pods.

It manages deployment and rollback of new application versions.

```sh
# deploy nginx via deployment action
kubectl apply -f nginx-deployment.yaml

# check deployment status
kubectl get all
# NAME                                READY   STATUS    RESTARTS   AGE
# pod/nginx-deploy-6d476dfb6f-7p9ct   1/1     Running   0          27s
# pod/nginx-deploy-6d476dfb6f-fnlvt   1/1     Running   0          27s
#
# NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3d5h
#
# NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/nginx-deploy   2/2     2            2           27s
#
# NAME                                      DESIRED   CURRENT   READY   AGE
# replicaset.apps/nginx-deploy-6d476dfb6f   2         2         2       27s

# list pods
kubectl get pods
# NAME                            READY   STATUS    RESTARTS   AGE
# nginx-deploy-6d476dfb6f-7p9ct   1/1     Running   0          2m45s
# nginx-deploy-6d476dfb6f-fnlvt   1/1     Running   0          2m45s

# list replica sets
kubectl get rs
# NAME                      DESIRED   CURRENT   READY   AGE
# nginx-deploy-6d476dfb6f   2         2         2       3m54s

# list deployments
kubectl get deploy
# NAME           READY   UP-TO-DATE   AVAILABLE   AGE
# nginx-deploy   2/2     2            2           4m52s

# detailed view of the deploy
kubectl describe deployment nginx-deploy
# Name:                   nginx-deploy
# Namespace:              default
# CreationTimestamp:      Sun, 23 Oct 2022 03:36:50 +0000
# Labels:                 <none>
# Annotations:            deployment.kubernetes.io/revision: 1
# Selector:               app=nginx1
# Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable
# StrategyType:           RollingUpdate
# MinReadySeconds:        0
# RollingUpdateStrategy:  25% max unavailable, 25% max surge
# Pod Template:
#   Labels:  app=nginx1
#   Containers:
#    nginx-container:
#     Image:      nginx
#     Port:       80/TCP
#     Host Port:  0/TCP
#     Limits:
#       cpu:        500m
#       memory:     128Mi
#     Environment:  <none>
#     Mounts:       <none>
#   Volumes:        <none>
# Conditions:
#   Type           Status  Reason
#   ----           ------  ------
#   Available      True    MinimumReplicasAvailable
#   Progressing    True    NewReplicaSetAvailable
# OldReplicaSets:  <none>
# NewReplicaSet:   nginx-deploy-6d476dfb6f (2/2 replicas created)
# Events:
#   Type    Reason             Age    From                   Message
#   ----    ------             ----   ----                   -------
#   Normal  ScalingReplicaSet  6m18s  deployment-controller  Scaled up replica set nginx-deploy-6d476dfb6f to 2

# scale up to 3 pods
kubectl scale deployment nginx-deploy --replicas 3

# list new pods
kubectl get all
# NAME                                READY   STATUS    RESTARTS   AGE
# pod/nginx-deploy-6d476dfb6f-55gql   1/1     Running   0          4s
# pod/nginx-deploy-6d476dfb6f-7p9ct   1/1     Running   0          9m4s
# pod/nginx-deploy-6d476dfb6f-fnlvt   1/1     Running   0          9m4s
#
# NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   3d5h
#
# NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/nginx-deploy   3/3     3            3           9m4s
#
# NAME                                      DESIRED   CURRENT   READY   AGE
# replicaset.apps/nginx-deploy-6d476dfb6f   3         3         3       9m4s
```

To update the deployment, just change `nginx-deployment.yaml` and run **apply** action over it again.

```sh
kubectl apply -f nginx-deployment.yaml
```

To rollback, just run `kubectl rollout undo deploy nginx-deploy -n default`

To delete the deployment type `kubectl delete deployment nginx-deploy`

## Using Service for access control

Services enable general access and load balancing of deployments.

First, deploy the application:

```sh
# deploy apache server
kubectl apply -f apache-deploy.yaml

# list deploy
kubectl get deploy
# NAME            READY   UP-TO-DATE   AVAILABLE   AGE
# apache-deploy   3/3     3            3           7h55m

# list pods and IPs
kubectl get pod -o wide
# NAME                             READY   STATUS    RESTARTS   AGE     IP           NODE       NOMINATED NODE   READINESS GATES
# apache-deploy-664d5c7c59-68wks   1/1     Running   0          7h56m   172.17.0.5   minikube   <none>           <none>
# apache-deploy-664d5c7c59-pdbss   1/1     Running   0          7h56m   172.17.0.4   minikube   <none>           <none>
# apache-deploy-664d5c7c59-srz6x   1/1     Running   0          7h56m   172.17.0.3   minikube   <none>           <none>
```

Then, the service is enabled to access it:

```sh
# create apache service
kubectl apply -f apache-service.yaml

# list services
kubectl get svc
# NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# apache-service   ClusterIP   10.106.40.233   <none>        8080/TCP   54s
# kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP    4d3h

# describe the apache service
kubectl describe svc apache-service
# Name:              apache-service
# Namespace:         default
# Labels:            <none>
# Annotations:       <none>
# Selector:          app=apache-deploy
# Type:              ClusterIP
# IP Family Policy:  SingleStack
# IP Families:       IPv4
# IP:                10.106.40.233
# IPs:               10.106.40.233
# Port:              <unset>  8080/TCP
# TargetPort:        8080/TCP
# Endpoints:         <none>
# Session Affinity:  None
# Events:            <none>

```
