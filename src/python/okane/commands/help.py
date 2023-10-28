def get_cmd_flags():
    return ["-h", "--help"]


def get_help_usage_str(application_cmd="okane"):
    return f"\t{application_cmd} -h : Show this help text\n"


def execute(args, extra_args, controller):
    application_name = "Okane"
    application_cmd = "okane"
    help_txt = f"{application_name} command.\nUsage:\n"

    for cmd in controller.available_commands:
        if len(extra_args.keys()) > 1:
            cmd_flags = cmd.get_cmd_flags()
            for cmd_flag in cmd_flags:
                if cmd_flag in extra_args:
                    help_txt += cmd.get_help_usage_str(application_cmd)        
                    break
        else:
            help_txt += cmd.get_help_usage_str(application_cmd)

    print(help_txt)
