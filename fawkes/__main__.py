import argparse

from fawkes.cli import cli

def main():
    # Init the arg parser
    parser = argparse.ArgumentParser()
    # Defining all the arguments
    cli.define_arguments(parser)
    # Extracting all the arguments
    args = parser.parse_args()

    # Depending on the args, we execute the commands
    action = args.action
    fawkes_config_file = args.fawkes_config
    app_config_file = args.app_config
    query_term = args.query
    query_response_file_format = args.format

    # Initialise the logger
    cli.init_logger()

    # Run the action
    cli.run_action(
        action,
        fawkes_config_file,
        app_config_file,
        query_term,
        query_response_file_format,
    )

if __name__ == "__main__":
    main()