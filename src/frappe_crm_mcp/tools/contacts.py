"""Contact operations for Frappe CRM."""

from typing import Annotated, Any, Callable

from fastmcp import FastMCP

from frappe_crm_mcp.client import FrappeClient


def register(mcp: FastMCP, get_client: Callable[[], FrappeClient]) -> None:
    """Register contact tools with the MCP server."""

    @mcp.tool(annotations={"readOnlyHint": True})
    async def contacts_search(
        query: Annotated[str | None, "Search by name or email"] = None,
        organization: Annotated[str | None, "Filter by organization/company"] = None,
        limit: Annotated[int, "Maximum number of contacts to return"] = 20,
    ) -> list[dict[str, Any]]:
        """Search for contacts.

        Search contacts by name, email, or filter by organization.
        """
        client = get_client()
        filters: dict[str, Any] = {}
        if query:
            filters["full_name"] = ["like", f"%{query}%"]
        if organization:
            filters["company_name"] = ["like", f"%{organization}%"]

        return await client.get_list(
            "Contact",
            filters=filters or None,
            fields=[
                "name",
                "full_name",
                "email_id",
                "mobile_no",
                "phone",
                "company_name",
                "modified",
            ],
            order_by="modified desc",
            limit=limit,
        )

    @mcp.tool(annotations={"readOnlyHint": True})
    async def contacts_get(
        name: Annotated[str, "The contact ID"],
    ) -> dict[str, Any]:
        """Get a single contact by ID.

        Returns full contact details including all phone numbers and emails.
        """
        client = get_client()
        return await client.get_doc("Contact", name)

    @mcp.tool(annotations={"readOnlyHint": True})
    async def contacts_get_deals(
        contact: Annotated[str, "The contact ID"],
    ) -> Any:
        """Get all deals linked to a contact.

        Returns deals where this contact is involved.
        """
        client = get_client()
        return await client.call_method(
            "crm.api.contact.get_linked_deals",
            contact=contact,
        )
