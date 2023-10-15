import re
from app.user.models import User

from core.exceptions import (
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
)

def email_validation(email: str):
    # is_email_valid = re.match(r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b", email)
    # return re.match("(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])", email)
    return re.match("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email)

def phone_validation(phone: str):
    return re.match("^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$", phone)


def validation(
    email: str,
    phone: str,
    country: str = None,
) -> list:
    email = None if email=="" else email
    phone = None if phone=="" else phone
    if email != None:
        if not email_validation(email):
            print ("invalid_email")
            raise BadRequestException(message="Error: invalid email.")
    if phone != None:
        if not phone_validation(phone):
            print ("invalid_phone")
            raise BadRequestException(message="Error: invalid phone number.")
    if not email and not phone:
        print ("email_or_phone_required")
        raise BadRequestException(message="Email or phone number is required.")
    if phone != None:
        phone = '+'+''.join(filter(str.isdigit, phone))
    return [email, phone]

def user_availability(
    user: User,
) -> bool:
    if not user:
        print ("user_not_found")
        raise NotFoundException(message="Error: user not found.")
    if user.deleted_at:
        print ("user_not_available")
        raise BadRequestException(message="Error: user not available.")
    if user.user_type!="member" and user.user_type!="admin":
        print ("access_permission_error")
        raise UnauthorizedException(message="Access denied: only members can access.")
    return True