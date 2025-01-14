# Copyright 2020 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Output action."""
import logging

from mrack.actions.action import Action
from mrack.context import global_context
from mrack.errors import MetadataError
from mrack.outputs.ansible_inventory import AnsibleInventoryOutput
from mrack.outputs.pytest_multihost import PytestMultihostOutput

logger = logging.getLogger(__name__)


class Output(Action):
    """
    Output action.

    Test action to run output modules from data in database.
    """

    def __init__(
        self,
        config=None,
        metadata=None,
        db_driver=None,
        ansible_path=None,
        pytest_multihost_path=None,
    ):  # pylint: disable=arguments-differ
        """Initialize the Output action."""
        super().__init__(config=config, metadata=metadata, db_driver=db_driver)

        if global_context.CONFIG:
            global_ansible_path = global_context.CONFIG.ansible_inventory_path()
            global_multihost_path = global_context.CONFIG.pytest_multihost_path()
        else:
            global_ansible_path = None
            global_multihost_path = None

        self._ansible_path = ansible_path or global_ansible_path
        self._pytest_multihost_path = pytest_multihost_path or global_multihost_path

    async def generate_outputs(self):
        """Generate outputs."""
        logger.info("Output generation started")

        if not self._db_driver.hosts:
            raise MetadataError("No hosts found.")

        ansible_o = AnsibleInventoryOutput(
            self._config, self._db_driver, self._metadata, self._ansible_path
        )
        multihost_o = PytestMultihostOutput(
            self._config, self._db_driver, self._metadata, self._pytest_multihost_path
        )

        ansible_o.create_output()
        multihost_o.create_output()

        logger.info("Output generation done")
        return True
