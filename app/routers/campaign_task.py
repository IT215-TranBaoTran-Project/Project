from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="",
    tags=["Campaign Tasks"]
)


@router.get("/campaign-tasks/{task_id}")
def get_campaign_task(task_id: int):
    if task_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Mã công việc không hợp lệ"
        )

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy công việc"
    )