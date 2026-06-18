import importlib
import pkgutil
import structlog
from typing import List

logger = structlog.get_logger()

def discover_tools(package_names: List[str] = ["tools.search.tools", "tools.fetch.tools", "tools.analyze.tools", "tools.write.tools"]):
    """
    Import tool modules to trigger registration via @tool decorator.
    """
    for module_name in package_names:
        try:
            importlib.import_module(module_name)
            logger.info("tools_module_loaded", module=module_name)
        except ImportError as e:
            logger.error("failed_to_load_tools_module", module=module_name, error=str(e))
