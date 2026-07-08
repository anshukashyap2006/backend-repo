class ApiResponse:
    def __init__(self,
        status_code: int,
        data: dict = {},
        message:str = "Success",
    ):
        self.status_code = status_code
        self.message = message
        self.data = data
        self.success = status_code
        