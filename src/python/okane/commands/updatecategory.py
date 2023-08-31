
def get_cmd_flags():
    return ["-uc", "--update-category"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -ua <id of existent category>: update an category\n"
    help_usage_str += f"\t{application_cmd} --update-category <id of existent category>: update an category\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 2:
        cat_id = int(args[0])
        category = controller.categoryDAO.getCategoryFromId(cat_id)
        if category is None or category.id < 0:
            print("It couldn't find category with the given id: " + str(cat_id))
        category.name = args[1]
        controller.categoryDAO.updateCategory(category)
