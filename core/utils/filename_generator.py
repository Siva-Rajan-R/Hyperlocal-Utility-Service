from hyperlocal_platform.core.utils.uuid_generator import generate_uuid
from icecream import ic
from typing import Optional,List


def generate_unq_filename(extenstion:str,prfix_name:Optional[str]="",suffix_name:Optional[str]=""):
    unq_filename=f"{prfix_name}-{generate_uuid()}-{suffix_name}.{extenstion}"
    ic(unq_filename)
    return unq_filename