from okane.utils import utils

def get_cmd_flags():
    return ["-dc", "--delete-category"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -dc <new-category-to-be-deleted>: delete a category\n"
    help_usage_str += f"\t{application_cmd} --delete-category <new-category-to-be-deleted>: delete a category\n"
    return help_usage_str


def execute(args, extra_args, controller):
    """
    Deletes a category from the database.

    Args:
        args (list): A list of arguments passed to the command.
        extra_args (list): A list of extra arguments passed to the command.
        controller (Controller): An instance of the Controller class.

    Returns:
        None
    """
    if len(args) > 0:
        for arg in args:
            if utils.is_int(arg):
                cat_id = int(arg)
                category = controller.categoryDAO.getCategoryFromId(cat_id)
            else:
                category_name = arg
                category = controller.categoryDAO.getCategory(category_name)
            if category is None or category.id < 0:
                print("It couldn't find category with the given parameter: " + arg)
                return

            controller.categoryDAO.delete(category)
            print("Category deleted!")
            category.print_properties()
    else:
        print("Missing category name")
        print("Usage: python -m okane -dc <new-category-to-be-deleted>")
