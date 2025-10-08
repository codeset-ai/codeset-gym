from typing import Dict, Any

import junitparser
from docker.models.containers import Container

from .base import TestResultCollector


class RustTestResultCollector(TestResultCollector):
    """Test result collector for Rust projects."""

    def get_test_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """
        Get test results from Rust projects using cargo2junit.

        Args:
            instance_id: The instance ID being processed
            container: Docker container instance

        Returns:
            JUnitXml test suite from cargo2junit

        Raises:
            Exception: If test results cannot be retrieved
        """
        test_path = "target/nextest/junit.xml"
        return self._get_single_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )
