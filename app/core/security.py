import bcrypt

def hash_password(password: str, cost_factor: int = 12) -> str:
    """
    Băm mật khẩu sử dụng thư viện bcrypt trực tiếp.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=cost_factor)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Kiểm tra mật khẩu người dùng nhập vào có khớp với mật khẩu đã băm trong DB hay không.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)