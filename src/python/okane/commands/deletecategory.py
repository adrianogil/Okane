from okane.utils import utils

def get_cmd_flags():
    return ["-dc", "--delete-category"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -dc <new-category-to-be-deleted>: delete a category\n"
    help_usage_str += f"\t{application_cmd} --delete-category <new-category-to-be-deleted>: delete a category\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 1:
        if utils.is_int(args[0]):
            cat_id = int(args[0])
            category = controller.categoryDAO.getCategoryFromId(cat_id)
        else:
            category_name = args[0]
            category = controller.categoryDAO.getCategory(category_name)
        if category is None or category.id < 0:
            print("It couldn't find category with the given parameter: " + args[0])
            return

        controller.categoryDAO.delete(category)
        print("Account deleted!")
        category.print_properties()
    else:
        print("Missing category name")
        print("Usage: python -m okane -da <new-category-to-be-deleted>")
