#!/usr/bin/python3
"""Extract configuration from devices using NAPALM.

We loop through our inventory and get data from the devices based on task.host.
"""

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file

__author__ = "Hugo Tinoco"
__email__ = "hugotinoco@icloud.com"

nr = InitNornir("config.yml")


def get_device_facts_config(task):
    """Extract facts & configuration from devices with NAPALM's help."""
    facts = task.run(task=napalm_get, getters="get_facts")
    configs = task.run(task=napalm_get, getters="get_config")

    # Store config in host_vars
    task.host["facts"] = facts.result
    task.host["config"] = configs.result["get_config"]["running"]


def write_facts_config(task):
    """Dump facts & configuration to file."""
    facts = task.host["facts"]
    config = task.host["config"]

    asn = task.host["asn"]

    # Capture NAPALM FACTS
    write_file(
        task,
        filename=f"napalm_getters/ASN{asn}/facts/{task.host}.cfg",
        content=str(facts),
    )
    # CAPTURE CONFIGS PER ASN
    write_file(
        task,
        filename=f"napalm_getters/ASN{asn}/configs/{task.host}.cfg",
        content=str(config),
    )
    # CAPTURE A FULL VIEW OF THE NETWORK FOR BATFISH
    write_file(
        task,
        filename=f"napalm_getters/mpls_sdn_era/configs/{task.host}.cfg",
        content=str(config),
    )


def main():
    """Execute the nornir runbook."""
    nr.run(task=get_device_facts_config)
    print_result(nr.run(task=write_facts_config))


if __name__ == "__main__":
    main()
