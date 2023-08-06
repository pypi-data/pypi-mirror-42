# Airmail

> A CLI tool for deploying projects to AWS

## Introduction/Philosophy

The point of Airmail is to make deploying projects into AWS a little easier. It was inspired as a binding layer between [Terraformed](https://www.terraform.io/) infrastructure and deploying applications to [AWS ECS](https://docs.aws.amazon.com/ecs/index.html). At NYMag we wanted to manage infrastructure with Terraform and then allow applications to be more declarative about how they run without caring about the infrastructure. A developer should be able to change easily declare where and how their application will run and then be able to easily configure resources in Terraform to support that. Airmail is designed to deploy code _with the assumption that the underlying infrastructure is there to support the project_.

## How To

Airmail needs to be run in a project with a `.deploy` directory. It will look inside this directory for configuration files that will tell the tool how to deploy to ECS.

    <project dir>
    ├── app                     # The directory of your application
    ├── .deploy                 # The directory holding the config
    │   ├── config.yml          # Holds the primary config declarations
    │   └── <env>.env           # Environment variable configuration for the container
    └── ...

### Config File

The `config.yml` file contains all the information that Airmail needs to build the service and task definitions to deploy to ECS. [For an example file click here](https://github.com/nymag/airmail/blob/master/docs/config.md).

### Commands

A list of commands and corresponding arguments/environment variables [can be found here](https://github.com/nymag/airmail/blob/master/docs/commands/README.md).

### AWS Configuration

Airmail assumes your local env is configured per [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration) configuration. The tool uses Boto3 to execute requests to AWS and does not do anything to setup your local environment.

### Environment Variables

You can use a few environment variables to control how Airmail is run.

- `AWS_PROFILE`: will run the Boto3 commands under the local profile you have configured
- `AIRMAIL_ENV`: automatically chooses which environment to run commands for. Good for CI/CD so the prompt is not triggered.
- `AIRMAIL_DRY_RUN`: will run all of the command except the actual call to AWS
- `AIRMAIL_CONFIG_FILE` _(default: `config.yml`)_: specifies the file to read from in the `.deploy` directory for application configuration. The file must be a valid YAML file.
- `AIRMAIL_VERBOSE`: will log in verbose mode. Good for debugging.

## Local Development

Clone and run `python3 setup.py install` or download [Watchcode](https://github.com/bluenote10/watchcode) and run `watchcode` in the root of the project./
