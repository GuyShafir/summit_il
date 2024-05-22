from __future__ import annotations

import sys
from typing import Any

import functions_framework
from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1


@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)

    print(request_json['vm'], request_json['zone'], request_json['project'])

    change_machine_type(request_json['project'], request_json['zone'], request_json['vm'])


def wait_for_extended_operation(
        operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result


def change_machine_type(
        project_id: str, zone: str, instance_name: str,
) -> None:
    print('Shutting down', instance_name)
    terminate_instance(project_id, zone, instance_name
                       )
    types = {}

    machine_type = get_current_machine_type(project_id, zone, instance_name)

    with open('types.txt') as f:
        lines = f.readlines()

    for line in lines:
        origin = line.split(':')[0]
        target = line.split(':')[1]
        types[origin] = target

    new_vm_type = types[machine_type]
    print('changing', instance_name, new_vm_type)

    client = compute_v1.InstancesClient()
    instance = client.get(project=project_id, zone=zone, instance=instance_name)

    if instance.status != compute_v1.Instance.Status.TERMINATED.name:
        raise RuntimeError(
            f"Only machines in TERMINATED state can have their machine type changed. "
            f"{instance.name} is in {instance.status}({instance.status_message}) state."
        )

    machine_type = compute_v1.InstancesSetMachineTypeRequest()
    machine_type.machine_type = (
        f"projects/{project_id}/zones/{zone}/machineTypes/{new_vm_type}"
    )
    operation = client.set_machine_type(
        project=project_id,
        zone=zone,
        instance=instance_name,
        instances_set_machine_type_request_resource=machine_type,
    )

    wait_for_extended_operation(operation, "changing machine type")

    turn_on_instance(project_id, zone, instance_name)


def terminate_instance(project_id: str, zone: str, instance_name: str) -> None:
    client = compute_v1.InstancesClient()
    instance = client.get(project=project_id, zone=zone, instance=instance_name)

    if instance.status == compute_v1.Instance.Status.TERMINATED.name:
        print(f"{instance.name} is already in TERMINATED state.")
        return

    operation = client.stop(project=project_id, zone=zone, instance=instance_name)

    wait_for_extended_operation(operation, "terminating instance")


def turn_on_instance(project_id: str, zone: str, instance_name: str) -> None:
    client = compute_v1.InstancesClient()
    instance = client.get(project=project_id, zone=zone, instance=instance_name)

    if instance.status == compute_v1.Instance.Status.RUNNING.name:
        print(f"{instance.name} is already in RUNNING state.")
        return

    operation = client.start(project=project_id, zone=zone, instance=instance_name)

    wait_for_extended_operation(operation, "starting instance")


def get_current_machine_type(project_id: str, zone: str, instance_name: str) -> str:
    client = compute_v1.InstancesClient()
    instance = client.get(project=project_id, zone=zone, instance=instance_name)
    return instance.machine_type.split("/")[-1]
