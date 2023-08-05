"""
    Fitchain connector - Fitchain SDK

    Client application to connect to the fitchain API
    Compatible with Python2,2.7,3.x

    :copyright: (c) 2018 fitchain.io
"""
import requests
import yaml
from pathlib import Path
from fitchain import dummy_data as dd
from fitchain.project import Project
import json
import os
from fitchain.dummy_data import resolve


class Runtime:
    def __init__(self):
        """
        Read the .fitchain yaml file to see which project we are dealing with.
        Initialize the runtime.

        In case of being ran within a fitchain workspace, the .fitchain yaml file is being read. That file contains
        the address, workspace ID and the project id we are working on.

        In case of being ran inside a pod, a .project file should exist containing the project information.

        """
        self.result_dir = Path('/data/out')

        self.data_path = Path("./.data")
        if not self.data_path.is_dir():
            os.mkdir(self.data_path)

        self.build_path = Path("./.build")
        if not self.build_path.is_dir():
            os.mkdir(self.build_path)

        fitchain_file = Path("./.fitchain")
        project_file = Path("./.project")

        print("Working from " + os.getcwd())

        if project_file.is_file():
            print("Loading project from .project")
            data = json.load(open(project_file))
            self.project = Project(**data)

        elif fitchain_file.is_file():
            print("Loading project from .fitchain")
            config = yaml.load(open(fitchain_file))

            if config["pod"] is None:
                raise ValueError("No pod address has been set within the config file")

            if config["projectId"] is None:
                raise ValueError("No projectId has been set within the config file")

            self._pod = Pod(config["pod"])
            self.project = self._pod.project(config["projectId"])

        else:
            raise ValueError("The current directory is not a fitchain workspace!")

    def resolve(self, dataset_id):
        """
        Load the dataset from the current project.

        On the data owner's POD, the actual dataset will be loaded, but anywhere else a fake dataset is generated based
        on the schema

        :param dataset_id: the id of the dataset to load.
        :return: a pandas dataset containing the data the program has access to.
        """



        ds = None
        for item in self.project.datasources:
            if item['id'] == dataset_id:
                ds = item

        if ds is None:
            raise ValueError("No datasource with id " + dataset_id + " found in project " + self.project.id)

        # -- Check if the data file is available within the data folder
        file = Path('%s/%s' % (self.data_path, dataset_id))

        schema = ds['schema']
        if schema is None:
            raise ValueError("Datasource " + dataset_id + " does not contain a valid schema")

        return resolve(schema, file)

        # return self.project.resolve(dataset_id)

    def pod(self):
        """
        Get the pod.

        :return: the pod instance, or None if you are running inside a pod
        """
        return self._pod


class Pod:
    def __init__(self, url="http://localhost:9400/v1"):
        self.base_url = url

    def identity(self):
        r = requests.get(self.base_url + '/gateway')

        return r.json()

    def project(self, id):
        r = requests.get(self.base_url + '/projects/' + id)

        return Project(**r.json())

    def projects(self, qry=""):
        r = requests.get(self.base_url + '/projects?q=' + qry)

        result = []
        for item in r.json():
            result.append(Project(**item))

        return result

    def workspaces(self):
        r = requests.get(self.base_url + '/workspaces')

        return r.json()

    def providers(self):
        r = requests.get(self.base_url + '/providers')

        return r.json()

    def datasources(self):
        r = requests.get(self.base_url + '/datasources')

        return r.json()

    def jobs(self):
        r = requests.get(self.base_url + '/jobs')

        return r.json()