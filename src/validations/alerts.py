from fastapi import HTTPException, status


def positive_time_interval(start_date, end_date):
    if start_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Starting date should be lower than ending date",
        )
