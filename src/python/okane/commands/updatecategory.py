
def get_cmd_flags():
    return ["-uc", "--update-category"]


def get_help_usage_str(application_cmd="okane"):
    help_usage_str = f"\t{application_cmd} -ua <id of existent category>: update an category\n"
    help_usage_str += f"\t{application_cmd} --update-category <id of existent category>: update an category\n"
    return help_usage_str


def execute(args, extra_args, controller):
    if len(args) == 0:
        print("Missing parameters")
        print(get_help_usage_str())
        return

    interactive_mode = len(args) == 1

    category_id = int(args[0])
    category = controller.categoryDAO.getCategoryFromId(category_id)
    if category is None or category.id < 0:
        print("It couldn't find category with the given id: " + str(category_id))
        return

    parent_category_name = ""
    if interactive_mode:
        new_name = input(f"Category name ({category.name}): ")
        if new_name:
            category.name = new_name
        parent_category_name = category.parent.name if category.parent is not None else ""
        parent_category_name = input(f"Parent category name ({parent_category_name}): ")
    else:
        new_name = args[1]
        category.name = new_name

        if len(args) > 1:
            parent_category_name = args[2]
    
    if parent_category_name:
        parent_category = controller.categoryDAO.getCategory(parent_category_name)
        if parent_category is None:
            print("It couldn't find category with the given name: " + parent_category_name)
            return
        else:
            category.parent = parent_category
    
    controller.categoryDAO.updateCategory(category)
