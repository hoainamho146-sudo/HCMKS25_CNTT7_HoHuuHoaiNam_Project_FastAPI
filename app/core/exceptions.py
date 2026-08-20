from fastapi import Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class NotFoundException(AppException):
    def __init__(self, message: str = "Tài nguyên không tồn tại"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class BadRequestException(AppException):
    def __init__(self, message: str = "Yêu cầu không hợp lệ"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)


class ForbiddenException(AppException):
    def __init__(self, message: str = "Bạn không có quyền thực hiện hành động này"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message)


# Exception Handler đăng ký với FastAPI để chuẩn hóa format response lỗi
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.message
        }
    )