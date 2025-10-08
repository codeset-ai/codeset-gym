from typing import Dict, Any

import junitparser
from docker.models.containers import Container

from .base import TestResultCollector


class GoTestResultCollector(TestResultCollector):
    """Test result collector for Go projects."""

    def get_test_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """
        Get test results from Go projects using go-junit-report.

        Args:
            instance_id: The instance ID being processed
            container: Docker container instance

        Returns:
            JUnitXml test suite from go-junit-report

        Raises:
            Exception: If test results cannot be retrieved
        """
        test_path = "test-results"
        return self._get_single_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )
