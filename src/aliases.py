from datetime import datetime
from typing import Annotated, TypeAlias

from fastapi import Query

DatetimeOrNoneQuery: TypeAlias = Annotated[
    datetime | None, Query(examples=["2023-08-30T16:39:13.401Z"])
]
