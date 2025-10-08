from typing import Dict, Any

import junitparser
from docker.models.containers import Container

from .base import TestResultCollector


class JavaTestResultCollector(TestResultCollector):
    """Test result collector for Java projects."""

    def get_test_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """
        Get test results from Java projects, trying Maven first, then Gradle.

        Args:
            instance_id: The instance ID being processed
            container: Docker container instance

        Returns:
            JUnitXml test suite from either Maven or Gradle

        Raises:
            RuntimeError: If both Maven and Gradle methods fail
        """
        try:
            return self._get_maven_results(instance_id, container)
        except Exception as maven_error:
            try:
                return self._get_gradle_results(instance_id, container)
            except Exception as gradle_error:
                error_msg = f"Failed to get test results for {instance_id}. "
                error_msg += f"Maven method failed: {maven_error}. "
                error_msg += f"Gradle method failed: {gradle_error}"
                raise RuntimeError(error_msg)

    def _get_maven_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """Get test results from Maven surefire reports."""
        test_path = "target/surefire-reports"
        return self._get_multiple_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )

    def _get_gradle_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """Get test results from Gradle test results."""
        test_path = "build/test-results/test"
        return self._get_multiple_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )
