from typing import Dict, Any

import junitparser
from docker.models.containers import Container

from .base import TestResultCollector


class CppTestResultCollector(TestResultCollector):
    """Test result collector for C/C++ projects."""

    def get_test_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """
        Get test results from C/C++ projects using CMake with CTest.

        Args:
            instance_id: The instance ID being processed
            container: Docker container instance

        Returns:
            JUnitXml test suite from CTest

        Raises:
            Exception: If test results cannot be retrieved
        """
        repository = self._get_repository(instance_id)

        try:
            return self._get_ctest_results(instance_id, container)
        except Exception as ctest_error:
            try:
                return self._get_cmake_test_results(instance_id, container)
            except Exception as cmake_error:
                error_msg = f"Failed to get test results for {instance_id}. "
                error_msg += f"CTest method failed: {ctest_error}. "
                error_msg += f"CMake method failed: {cmake_error}"
                raise RuntimeError(error_msg)

    def _get_ctest_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """Get test results from CTest XML output."""
        # CTest's native XML output is always in /Testing directory (standard CTest location)
        return self._get_multiple_xml_from_archive(instance_id, container, "/Testing")

    def _get_cmake_test_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """Get test results from CMake test output."""
        test_path = "build/test-results"
        return self._get_single_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )
