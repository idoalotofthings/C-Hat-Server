import enum

class Event(enum.Enum):
    ON_START = 0
    ON_STOP = 1
    ON_MESSAGE = 2
    ON_USER_LOGIN = 3
    ON_USER_REGISTER = 4
    ON_CLIENT_CONNECT = 5
    ON_OTP_SENT = 6
    ON_EMAIL_VERIFY_FAIL = 7

