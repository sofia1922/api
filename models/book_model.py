from uuid import uuid4
from typing import Dict

def create_book_dict(data: Dict) -> Dict:
    return {
        "id": str(uuid4()),
        "title": data["title"],
        "author": data["author"],
        "description": data["description"],
        "status": data["status"],
        "year": data["year"]
    }