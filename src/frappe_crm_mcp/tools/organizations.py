"""Organization operations for Frappe CRM."""

from typing import Annotated, Any, Callable

from fastmcp import FastMCP

from frappe_crm_mcp.client import FrappeClient


def register(mcp: FastMCP, get_client: Callable[[], FrappeClient]) -> None:
    """Register organization tools with the MCP server."""

    @mcp.tool(annotations={"readOnlyHint": True})
    async def organizations_list(
        query: Annotated[str | None, "Search by organization name"] = None,
        industry: Annotated[str | None, "Filter by industry"] = None,
        limit: Annotated[int, "Maximum number of organizations to return"] = 20,
    ) -> list[dict[str, Any]]:
        """List organizations/companies in the CRM.

        Search by name or filter by industry.
        """
        client = get_client()
        filters: dict[str, Any] = {}
        if query:
            filters["organization_name"] = ["like", f"%{query}%"]
        if industry:
            filters["industry"] = industry

        return await client.get_list(
            "CRM Organization",
            filters=filters or None,
            fields=[
                "name",
                "organization_name",
                "industry",
                "website",
                "territory",
                "modified",
            ],
            order_by="modified desc",
            limit=limit,
        )

    @mcp.tool(annotations={"readOnlyHint": True})
    async def organizations_get(
        name: Annotated[str, "The organization ID"],
    ) -> dict[str, Any]:
        """Get a single organization by ID.

        Returns full organization details including address and contacts.
        """
        client = get_client()
        return await client.get_doc("CRM Organization", name)
