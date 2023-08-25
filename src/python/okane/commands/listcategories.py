
def get_cmd_flags():
    return ["-lc", "--list-categories"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -lc: list all categories\n"
    help_usage_str += f"\t{application_cmd} --list-categories: list all categories\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 0:
        category_list = controller.categoryDAO.getAll()
        for category in category_list:
            row_data = (category.id, category.name)
            # row_text = bcolors.OKBLUE + 'Id:' + bcolors.ENDC + ' %s\t' + \
            #            bcolors.OKBLUE + 'Category:' + bcolors.ENDC + ' %s'
            row_text = 'Id: %s\tCategory: %s'
            print(row_text % row_data )
