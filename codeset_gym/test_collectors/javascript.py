from typing import Dict, Any

import junitparser
from docker.models.containers import Container

from .base import TestResultCollector


class JavaScriptTestResultCollector(TestResultCollector):
    """Test result collector for JavaScript/TypeScript projects."""

    def get_test_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """
        Get test results from JavaScript projects, trying Jest, Mocha, then Vitest.

        Args:
            instance_id: The instance ID being processed
            container: Docker container instance

        Returns:
            JUnitXml test suite from Jest, Mocha, or Vitest

        Raises:
            RuntimeError: If all test frameworks fail
        """
        try:
            return self._get_jest_results(instance_id, container)
        except Exception as jest_error:
            try:
                return self._get_mocha_results(instance_id, container)
            except Exception as mocha_error:
                try:
                    return self._get_vitest_results(instance_id, container)
                except Exception as vitest_error:
                    error_msg = f"Failed to get test results for {instance_id}. "
                    error_msg += f"Jest method failed: {jest_error}. "
                    error_msg += f"Mocha method failed: {mocha_error}. "
                    error_msg += f"Vitest method failed: {vitest_error}"
                    raise RuntimeError(error_msg)

    def _get_jest_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """Get test results from Jest junit.xml."""
        test_path = "test-results/junit.xml"
        return self._get_single_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )

    def _get_mocha_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """Get test results from Mocha test-results.xml."""
        test_path = "test-results/test-results.xml"
        return self._get_single_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )

    def _get_vitest_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """Get test results from Vitest junit.xml."""
        test_path = "test-results/junit.xml"
        return self._get_single_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )
