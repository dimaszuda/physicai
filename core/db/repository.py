from typing import Any, Dict, Optional
from .connection import get_supabase


class BaseRepository:
    def __init__(self):
        self.client = get_supabase()

    def insert(self, table: str, data: Dict[str, Any]) -> Any:
        return self.client.table(table).insert(data).execute()

    def update(
        self, table: str, id_field: str, id_value: Any, data: Dict[str, Any]
    ) -> Any:
        return (
            self.client.table(table)
            .update(data)
            .eq(id_field, id_value)
            .execute()
        )

    def delete(self, table: str, id_field: str, id_value: Any) -> Any:
        return (
            self.client.table(table)
            .delete()
            .eq(id_field, id_value)
            .execute()
        )

    def select(
        self, table: str, filters: Optional[Dict[str, Any]] = None
    ) -> Any:
        query = self.client.table(table).select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        return query.execute()

