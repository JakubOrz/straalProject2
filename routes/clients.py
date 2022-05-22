from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def main_page():
    return """
        <h1> Tak działa strona główna </h1>
    """
