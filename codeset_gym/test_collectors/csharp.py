from typing import Dict, Any

import junitparser
from docker.models.containers import Container

from .base import TestResultCollector


class CSharpTestResultCollector(TestResultCollector):
    """Test result collector for C# projects."""

    def get_test_results(
        self, instance_id: str, container: Container
    ) -> junitparser.JUnitXml:
        """
        Get test results from C# projects using dotnet test with JUnit logger.

        Args:
            instance_id: The instance ID being processed
            container: Docker container instance

        Returns:
            JUnitXml test suite from dotnet test

        Raises:
            Exception: If test results cannot be retrieved
        """
        test_path = "TestResults"
        return self._get_multiple_xml_from_archive(
            instance_id, container, f"/{test_path}"
        )
