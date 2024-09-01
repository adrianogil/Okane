from okane.utils import utils

from pyutils.decorators import debug

def get_cmd_flags():
    return ["-dr", "--delete-recurrent"]

def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -dr <id-of-recurrent-register-to-be-deleted>: delete a recurrent register\n"
    help_usage_str += f"\t{application_cmd} --delete-recurrent <id-of-recurrent-register-to-be-deleted>: delete a recurrent register\n"
    return help_usage_str

def execute(args, extra_args, controller):
    if len(args) == 1 and utils.is_int(args[0]):
        recurrent_id = int(args[0])
        recurrentRegister = controller.recurrentMoneyDAO.getFromId(recurrent_id)
        if recurrentRegister is None or recurrentRegister.id < 0:
            print("It couldn't find a recurrent register with the given id.")
            return
        # TODO: delete all registers that are linked to this recurrent register
        controller.recurrentMoneyDAO.delete(recurrentRegister)
        print('Recurrent register deleted!')
    else:
        print("Missing recurrent register ID")
        print("Usage: python -m okane -dr <id-of-recurrent-register-to-be-deleted>")
