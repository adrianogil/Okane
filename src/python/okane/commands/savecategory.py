
def get_cmd_flags():
    return ["-sc", "--save-category"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -sc <new-category-to-be-created>: save a category\n"
    help_usage_str += f"\t{application_cmd} --save-category <new-category-to-be-created>: save a category\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 1:
        controller.categoryDAO.saveCategory(args[0])
        print("Category created!")
    else:
        print("Missing category name")
        print("Usage: python -m okane -ca <new-category-to-be-created>")
