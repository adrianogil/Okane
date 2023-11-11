
from okane.utils import utils


def get_cmd_flags():
    return ["-sc", "--save-category"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -sc <new-category-to-be-created> [<parent-category>]: save a category\n"
    help_usage_str += f"\t{application_cmd} --save-category <new-category-to-be-created> [<parent-category>]: save a category\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 0:
        print("Missing parameters")
        print("Usage: python -m okane -ca <new-category-to-be-created> [<parent-category>]")
        return

    category_name = args[0]
    category_parent = None

    category_args = {
        "name": category_name
    }

    if len(args) > 1:   
        arg2 = args[1]

        if utils.is_int(arg2):
            parent_id = arg2
            category_parent = controller.categoryDAO.getCategoryFromId(parent_id)
        else:
            parent_name = arg2
            category_parent = controller.categoryDAO.getCategory(parent_name)
    
    if category_parent:
        category_args["parent_id"] = category_parent.id

    controller.categoryDAO.saveCategory(**category_args)
    print("Category created!")
