from typing import Dict, Any, Callable
from .contracts import SystemContext

class ToolRouter:
    def __init__(self):
        self._routes: Dict[str, Callable] = {}

    def register_tool(self, name: str, handler: Callable):
        self._routes[name] = handler

    def route(self, context: SystemContext, step: Dict[str, Any]) -> Any:
        """
        Routes a planned step to the appropriate tool handler.
        Validates that the tool is in context.allowed_tools.
        """
        tool_name = step.get("tool")
        if not tool_name:
            raise ValueError("Tool name is required in step")
            
        if tool_name not in context.allowed_tools:
            raise PermissionError(f"Tool {tool_name} is not allowed in current context")
            
        handler = self._routes.get(tool_name)
        if not handler:
            raise NotImplementedError(f"Handler for tool {tool_name} not found")
            
        return handler(step)
