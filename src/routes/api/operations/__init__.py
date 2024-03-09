from fastapi import APIRouter

router = APIRouter(
    prefix="/operations"
)

@router.get("/getinfo")
async def get_info():
    pass

@router.post("/addinfo")
async def add_info():
    pass
