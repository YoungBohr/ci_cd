# -*- coding: utf-8 -*-

import yaml
import src.constants as C
from kubernetes import client, config

config.kube_config.load_kube_config(config_file=C.KUBE_CONFIG)
config.load_kube_config()

v1 = client.CoreV1Api


def get_pod(api_instance: client.core_v1_api.CoreV1Api, name: str, namespace: str):
    pod = api_instance.read_namespaced_pod(name=name, namespace=namespace)


def get_core_dns(pod_manifest, svc):
    pass
