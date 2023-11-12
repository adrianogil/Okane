
def get_cmd_flags():
    return ["-lc", "--list-categories"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -lc: list all categories\n"
    help_usage_str += f"\t{application_cmd} --list-categories: list all categories\n"
    return help_usage_str


def execute(args, extra_args, controller):
    """
    Executes the 'listcategories' command, which retrieves all categories from the database and prints them in a tree-like structure.

    Args:
        args: A list of command-line arguments.
        extra_args: A dictionary of extra arguments.
        controller: The controller object that handles interactions with the database.

    Returns:
        None
    """
    categories = controller.categoryDAO.getAll()
    category_dict = {category.id: (category.name, []) for category in categories}

    for category in categories:
        if category.parent is not None:
            category_dict[category.parent.id][1].append(category.id)

    def print_tree(category_id, indent=0):
        name, children = category_dict[category_id]
        print(' ' * indent + '- [%s] %s' % (category_id, name))
        for child_id in children:
            print_tree(child_id, indent + 2)

    root_categories = [category.id for category in categories if category.parent is None]
    for root in root_categories:
        print_tree(root)