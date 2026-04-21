# backend/app/crud/users.py

from sqlalchemy.orm import Session

from app.models.payment_methods import PaymentMethod
from app.models.user_payment_methods import UserPaymentMethod
from app.models.user_ranks import UserRank
from app.models.users import User
from app.schemas.users import UserCreateRequest


def create_user_with_default_payment_method(
    db: Session,
    data: UserCreateRequest,
    cognito_sub: str,
    email: str | None,
):

    if not email:
        raise ValueError("メールアドレスが取得できません")

    default_payment_method = (
        db.query(PaymentMethod)
        .filter(PaymentMethod.code == "cash_on_delivery")
        .filter(PaymentMethod.is_active == True)  # noqa: E712
        .first()
    )

    if not default_payment_method:
        raise ValueError("初期支払い方法が見つかりません")

    default_rank = db.query(UserRank).filter(UserRank.code == "normal_user").first()

    if not default_rank:
        raise ValueError("初期ユーザーランクが見つかりません")

    user = User(
        cognito_sub=cognito_sub,
        last_name=data.last_name,
        first_name=data.first_name,
        gender=data.gender,
        postal_code=data.postal_code,
        prefecture=data.prefecture,
        address1=data.address1,
        address2=data.address2,
        address3=data.address3,
        email=email,
        phone_number=data.phone_number,
        birthday=data.birthday,
        rank_id=default_rank.id,
    )

    db.add(user)
    db.flush()

    user_payment_method = UserPaymentMethod(
        user_id=user.id,
        payment_method_id=default_payment_method.id,
        provider="manual",
        is_default=True,
        is_active=True,
    )

    db.add(user_payment_method)
    db.commit()
    db.refresh(user)

    return user, default_payment_method
