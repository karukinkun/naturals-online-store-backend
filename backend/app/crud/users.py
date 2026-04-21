# backend/app/crud/users.py

from sqlalchemy.orm import Session, joinedload

from app.models.payment_methods import PaymentMethod
from app.models.user_payment_methods import UserPaymentMethod
from app.models.user_ranks import UserRank
from app.models.users import User
from app.schemas.users import UserCreateRequest
from app.utils.storage import build_image_url


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


DEFAULT_USER_RANK_ID = 1


def get_user_by_cognito_sub(
    db: Session,
    cognito_sub: str,
):
    user = (
        db.query(User)
        .options(
            joinedload(User.rank),
            joinedload(User.payment_methods).joinedload(
                UserPaymentMethod.payment_method
            ),
        )
        .filter(User.cognito_sub == cognito_sub)
        .filter(User.is_active == True)  # noqa: E712
        .first()
    )

    if not user:
        return None

    default_user_payment_method = next(
        (
            user_payment_method
            for user_payment_method in user.payment_methods
            if user_payment_method.is_default and user_payment_method.is_active
        ),
        None,
    )

    return {
        "id": user.id,
        "cognito_sub": user.cognito_sub,
        "last_name": user.last_name,
        "first_name": user.first_name,
        "gender": user.gender,
        "birthday": user.birthday,
        "postal_code": user.postal_code,
        "prefecture": user.prefecture,
        "address1": user.address1,
        "address2": user.address2,
        "address3": user.address3,
        "email": user.email,
        "phone_number": user.phone_number,
        "points": user.points,
        "rank": {
            "code": user.rank.code,
            "name": user.rank.name,
            "image_url": build_image_url(user.rank.image_url),
            "point_rate": user.rank.point_rate,
        }
        if user.rank
        else None,
        "default_payment_method": {
            "code": default_user_payment_method.payment_method.code,
            "name": default_user_payment_method.payment_method.name,
        }
        if default_user_payment_method and default_user_payment_method.payment_method
        else None,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }
