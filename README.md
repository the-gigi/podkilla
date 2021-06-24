# Podkilla

Podkilla kills Kubernetes pods. It scans all the pods in all the clusters listed in the clusters.txt file and deletes all the failed ones.
You can also specify a specific reason and then it will delete only the pods that failed with that particular reason.

# Requirements

This is a Python 3 program.

Make sure you have Python 3 installed:

```
$ brew install python
```  

Install `pyenv`:

```
brew install pyenv
```

Install `poetry`:

```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

Setup a virtual environment for the project:

```
pyenv install 3.9.4
pyenv local 3.9.4
poetry install 
```

Also, you need `kubectl` and a kube-config file with some clusters.

# Usage

Create a file called clusters.txt that contains the kube-contexts of your clusters from  your ~/.kube/config that you want Podkilla to operate on.

The file should look like:

```
gke_some-cluster
k3d-k3s-default
kind-kind
minikube
```

Then just run:

```
poetry run python podkilla.py
```

If you 