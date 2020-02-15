from app.models import User, UserSchema
from app import db

import username_generator


def create(user, cleartext_password):
    schema = UserSchema()
    new_user = schema.load(user, session=db.session)

    new_user.set_password(cleartext_password)

    db.session.add(new_user)
    db.session.commit()

    return new_user


def create_guest():
    username = username_generator.get_uname(3, 64, False)
    email = f"{username}@mailinator.com"
    cleartext_password = username
    user_dict = dict(username=username, email=email, is_guest=True)

    existing_user = get_user_by_name(username)
    if existing_user is None:
        return create(user_dict, cleartext_password)
    else:
        return existing_user


def get_user_by_name(username):
    return User.query.filter(User.username == username).one_or_none()


def get_user_by_email(email):
    return User.query.filter(User.email == email).one_or_none()


def get_user_by_id(user_id):
    return User.query.filter(User.user_id == user_id).one_or_none()


def verify_password_reset_token(token):
    return User.verify_password_reset_token(token)


def read_all():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)


def read_quota_list():
    """
    Returns a list of user dicts with essential information only, 
    sorted by bake quota (# cakes baked)/(# cakes eaten) from least baked to most baked.

    If no bakes were eaten, the quota is (# cakes baked) / 1
    """
    members = read_all()

    stripped_members = [
        {
            "username": member["username"],
            "user_id": member["user_id"],
            "eaten": len(member["sessions"]) + member["eaten_offset"],
            "baked": len(member["baker_sessions"]) + member["baked_offset"],
        }
        for member in members
    ]
    for member in stripped_members:
        member["quota"] = member["baked"] / max(member["eaten"], 1)

    return sorted(stripped_members, key=lambda x: x["quota"])
