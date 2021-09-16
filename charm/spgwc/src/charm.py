#!/usr/bin/env python3
# Copyright 2021 root
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class SpgwcCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.spgwc_pebble_ready, self._on_spgwc_pebble_ready)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.fortune_action, self._on_fortune_action)
        self.framework.observe(self.on.install, self._on_install)
        self._stored.set_default(things=[])

    def _on_spgwc_pebble_ready(self, event):
        """Define and start a workload using the Pebble API.

        TEMPLATE-TODO: change this example to suit your needs.
        You'll need to specify the right entrypoint and environment
        configuration for your specific workload. Tip: you can see the
        standard entrypoint of an existing container using docker inspect

        Learn more about Pebble layers at https://github.com/canonical/pebble
        """
        # Get a reference the container attribute on the PebbleReadyEvent
        container = event.workload
        # Define an initial Pebble layer configuration
        pebble_layer = {
            "summary": "spgwc layer",
            "description": "pebble config layer for httpbin",
            "services": {
                "spgwc": {
                    "override": "replace",
                    "summary": "spgwc",
                    "command": """/bin/bash -xc "/opt/cp/scripts/spgwc-run.sh" """,
                    "startup": "enabled",
                    "environment": {"thing": self.model.config["thing"]},
                }
            },
        }
        scriptPath = "/opt/cp/scripts/"
        scriptPath1 = "/etc/cp/config/"
        self._push_file_to_container(container, "src/files/script/*.*", scriptPath, 0o755)
        self._push_file_to_container(container, "src/files/config/*.*", scriptPath1, 0o755)

        # Add intial Pebble config layer using the Pebble API
        container.add_layer("spgwc", pebble_layer, combine=True)
        # Autostart any services that were defined with startup: enabled
        container.autostart()
        # Learn more about statuses in the SDK docs:
        # https://juju.is/docs/sdk/constructs#heading--statuses
        self.unit.status = ActiveStatus()

    def _on_config_changed(self, _):
        """Just an example to show how to deal with changed configuration.

        TEMPLATE-TODO: change this example to suit your needs.
        If you don't need to handle config, you can remove this method,
        the hook created in __init__.py for it, the corresponding test,
        and the config.py file.

        Learn more about config at https://juju.is/docs/sdk/config
        """
        current = self.config["thing"]
        if current not in self._stored.things:
            logger.debug("found a new thing: %r", current)
            self._stored.things.append(current)

    def _on_fortune_action(self, event):
        """Just an example to show how to receive actions.

        TEMPLATE-TODO: change this example to suit your needs.
        If you don't need to handle actions, you can remove this method,
        the hook created in __init__.py for it, the corresponding test,
        and the actions.py file.

        Learn more about actions at https://juju.is/docs/sdk/actions
        """
        fail = event.params["fail"]
        if fail:
            event.fail(fail)
        else:
            event.set_results({"fortune": "A bug in the code is worth two in the documentation."})


    def _push_file_to_container(self, container, srcPath, dstPath, filePermission):
        for filePath in glob.glob(srcPath):
            print("Loading file name:" + filePath)
            fileData = loadfile(filePath)
            fileName = os.path.basename(filePath)
            container.push(dstPath + fileName, fileData, make_dirs=True, permissions=filePermission)

    '''def _patch_k8s_service(self):
        """Fix the Kubernetes service that was setup by Juju with correct port numbers."""
        if self.unit.is_leader():
            service_ports = [
                (f"s6a", self._s6a_port, self._s6a_port),
                (f"config-port", self._config_port, self._config_port),
                (f"prometheus-exporter", self._prometheus_port, self._prometheus_port),
            ]
            try:
                K8sServicePatch.set_ports(self.app.name, service_ports)
            except PatchFailed as e:
                logger.error("Unable to patch the Kubernetes service: %s", str(e))
            else:
                logger.info("Successfully patched the Kubernetes service")'''

    def _on_install(self, _):
        """Event handler for InstallEvent during which we will update the K8s service."""
        
        """Handle the install event, create Kubernetes resources"""
        if not self._k8s_auth():
            event.defer()
            return
        self.unit.status = MaintenanceStatus("creating k8s resources")
        # Create the Kubernetes resources needed for the mme
        r = resources.SpgwcCharm(self)
        r.apply()


    '''def _on_upgrade_charm(self, _):
        """Event handler for replica's UpgradeCharmEvent."""
        # Ensure that older deployments of Alertmanager run the logic to patch the K8s service
        self._patch_k8s_service()

       # update config hash
        self._stored.config_hash = (
            ""
            if not self.container.can_connect()
            else sha256(yaml.safe_dump(yaml.safe_load(self.container.pull(self._config_path))))
        )

        # After upgrade (refresh), the unit ip address is not guaranteed to remain the same, and
        # the config may need update. Calling the common hook to update.
        self._common_exit_hook()'''



if __name__ == "__main__":
    main(SpgwcCharm)
