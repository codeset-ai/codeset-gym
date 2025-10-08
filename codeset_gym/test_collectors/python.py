from typing import Dict, Any

import junitparser
from docker.models.containers import Container

from .base import TestResultCollector


class PythonTestResultCollector(TestResultCollector):
    """Test result collector for Python projects."""

    def get_test_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """
        Get test results using pytest first, fallback to unittest if pytest fails.

        Args:
            instance_id: The instance ID being processed
            container: Docker container instance

        Returns:
            JUnitXml test suite from either pytest or unittest

        Raises:
            RuntimeError: If both pytest and unittest methods fail
        """
        try:
            return self._get_pytest_results(instance_id, container)
        except Exception as pytest_error:
            try:
                return self._get_unittest_results(instance_id, container)
            except Exception as unittest_error:
                error_msg = f"Failed to get test results for {instance_id}. "
                error_msg += f"Pytest method failed: {pytest_error}. "
                error_msg += f"Unittest method failed: {unittest_error}"
                raise RuntimeError(error_msg)

    def _get_pytest_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """Get test results from pytest XML report."""
        test_path = "report.xml"
        return self._get_single_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )

    def _get_unittest_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """Get test results from unittest XML reports in test_reports folder."""
        test_path = "test_reports"
        return self._get_multiple_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )
