from fastmcp import FastMCP

mcp = FastMCP("Markaz MCP Server")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def get_status() -> str:
    """Check server status"""
    return "Markaz MCP Server is running successfully!"

if __name__ == "__main__":
    mcp.run()