from sqlalchemy import func
from .domain import domain_exists
from .models import UsedQuota
from .mailbox import mailbox_exists
from .db import get_db_session
from .exc import NoSuchDomain, NoSuchMailbox


def get_domain_sum_used_quota(domain: str):
    if not domain_exists(domain):
        raise NoSuchDomain(domain)

    return get_db_session().query(
        func.sum(UsedQuota.bytes).label('bytes'), func.sum(UsedQuota.messages).label('messages'),
    ).filter_by(domain=domain).one()


def get_mailbox_sum_used_quota(email_address: str):
    if not mailbox_exists(email_address):
        raise NoSuchMailbox(email_address)

    return get_db_session().query(
        UsedQuota.bytes, UsedQuota.messages
    ).filter_by(username=email_address).one()


def get_domain_used_quota(domain: str):
    if not domain_exists(domain):
        raise NoSuchDomain(domain)
    return get_db_session().query(UsedQuota).filter_by(domain=domain).all()


def get_mailbox_used_quota(email_address: str):
    if not mailbox_exists(email_address):
        raise NoSuchMailbox(email_address)
    return get_db_session().query(UsedQuota).filter_by(username=email_address).one()


def delete_used_quota_mailbox(email_address):
    if not mailbox_exists(email_address):
        raise NoSuchMailbox(email_address)
    return get_db_session().query(UsedQuota).filter_by(username=email_address).delete() == 1


def reset_mailbox_used_quota(email_address):
    if not mailbox_exists(email_address):
        raise NoSuchMailbox(email_address)

    used_quota = get_mailbox_used_quota(email_address)
    used_quota.bytes = 0
    used_quota.messages = 0

    db_session = get_db_session()
    db_session.add(used_quota)
    db_session.flush()

    return True
