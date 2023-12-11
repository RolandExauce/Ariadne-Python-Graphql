from prisma.client import Prisma
from prisma.errors import PrismaError
from src.utils.errors_and_success_msgs import (
    custom_prisma_error_msgs, user_op_msgs,
    INVALID_DATE,
    UNKNOWN_ERR,
)
import bcrypt
import datetime

# Initialize a global Prisma instance
prisma = Prisma()
connected = False


# Get Prisma instance
async def get_prisma_instance():
    global connected
    try:
        if not connected:
            await prisma.connect()
            connected = True
        return prisma
    except PrismaError as e:
        return {"errorMsg": e.error_message}


# Validate birthdate format
def validate_birthdate_format(birthdate):
    try:
        year, month, day = map(int, birthdate.split("-"))
        current_year = datetime.datetime.now().year

        # Check if year is 4 characters long and not less than 1950
        if not (1950 <= year <= current_year and len(str(year)) == 4):
            return False

        # Check if month is in the valid range (1 to 12)
        if not 1 <= month <= 12:
            return False

        # Check for months with 30 days
        if month in [4, 6, 9, 11] and day > 30:
            return False

        # Check for February and leap year (Feb has 29 days on leap years)
        if month == 2:
            if day > 29:
                return False
            leap_year = (year % 4 == 0 and year %
                         100 != 0) or (year % 400 == 0)
            if not leap_year and day > 28:
                return False

        # Check for days in months with 31 days
        if day > 31:
            return False

        return True

    except (ValueError, IndexError):
        return False


# Create user
async def create_user_logic(user_data: dict):
    try:
        prisma_instance = await get_prisma_instance()

        if isinstance(prisma_instance, dict) and "custom_error" in prisma_instance:
            return {"custom_error": prisma_instance.get("custom_error")}

        prisma = prisma_instance

        # Validating birthdate format
        birthdate = user_data.get("birthdate")
        if not validate_birthdate_format(birthdate):
            return {"custom_error": INVALID_DATE}

        hashed_password = bcrypt.hashpw(
            str(user_data["password"]).encode(), bcrypt.gensalt()).decode()

        user_data["password"] = hashed_password

        created_user = await prisma.user.create(data=user_data)
        return {"message": user_op_msgs(op="CREATE")} if created_user else {
            "custom_error": user_op_msgs(op="CREATE", caseErr="FAILED")
        }
    except Exception as e:
        error_message = custom_prisma_error_msgs(str(e))
        return {"custom_error": f"Failed: {error_message}" if error_message else UNKNOWN_ERR}
