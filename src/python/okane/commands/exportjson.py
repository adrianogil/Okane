from okane.args import ARGS
from okane.utils import utils

from pyutils.utils.jsonutils import write_to_file


def get_cmd_flags():
    return ["-ej", "--export-json"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -ej <path-json-to-be-saved>: export a json file\n"
    help_usage_str += f"\t{application_cmd} --export-json <path-json-to-be-saved>: export a json file\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) > 0:
        filename = args[0]
    else:
        filename = 'data.json'

    dao_args = extra_args.copy()

    for a in args:
        if utils.is_int(a):
            number = int(a)
            if number < 0:
                dao_args['limit'] = str((-1) * number)
            else:
                dao_args['offset'] = str(number)

    if ARGS.category in extra_args:
        category_conditions = []
        for c in extra_args[ARGS.category]:
            category_conditions.append(controller.get_category_from({ARGS.category : [c]})[1])
        dao_args['categories'] = category_conditions

    register_list = controller.moneyDAO.getAll(dao_args)

    okane_data = {}

    money_registers = []
    for money in register_list:
        row_data = {
            'MoneyId': money.id,
            'Date': str(money.register_dt),
            'Amount': money.amount,
            'Description': money.description,
            'Category': money.category.name,
            'Account': money.account.name,
            'Confirmed': money.confirmed
        }
        money_registers.append(row_data)

    okane_data["OkaneData"] = {
        "MoneyRegisters": money_registers
    }

    write_to_file(filename, okane_data)
