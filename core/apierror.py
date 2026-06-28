from typing import List,Any,Optional


class ApiError(Exception):
    """
    a custom api error class to standardise the api error response 
    mainly for the frontend so that they can understand the error better if there is any problem
    """
    def __init__(self,
        status_code: int,
        message: str = "Something went wrong",
        error : Optional[List[Any]] = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.success = False
        self.error = error or []
        self.data = None



        