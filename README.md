# Big Data with PySpark

Bla bla bla.

Reference: <>

## Install Java (Spark Dependency)

- Install Java JRE: `apt install default-jre`

## Python Base Install (Virtual Environment - venv)

Using python virtual environment.

- Check existing python install: `apt list python3 -a`
- Install pip: `apt install python3-pip`
- Install virtual environment package: `apt install python3-venv`
- Create a virtual environment: `python3 -m venv env`
- Add `.gitignore` with the line `env` to skip it on SCM
- Start virtual environment: `source env/bin/activate`
- List existing modules in the virtual environment: `pip list -v`
- Stop virtual environment: `deactivate`

## Python modules Install

### Jupyter Notebook

With virtual environment enabled.

- Install Jupyter: `pip install jupyter`
- List existing modules in the virtual environment: `pip list -v`
- Startup Jupyter Notebook: `jupyter notebook`

## Install Spark

Install Spark as a global install.

```shell
wget https://dlcdn.apache.org/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz
sudo mkdir /usr/local/bin/spark
sudo chown <user>. /usr/local/bin/spark
tar -xf spark-3.3.0-bin-hadoop3.tgz -C /usr/local/bin/spark
```

Setup environment variables at your .bashrc or .zshrc or ...

```shell
export SPARK_HOME=/usr/local/bin/spark/spark-3.3.0-bin-hadoop3
export PATH=$PATH:$SPARK_HOME/$SPARK_HOME/bin:$SPARK_HOME/python
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS=notebook
export PYSPARK_PYTHON=python3
```
