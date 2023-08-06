import os
import click
import boto3
import json
from airmail.cli import pass_context
from airmail.services.ecs_service import ECSService

@click.group(short_help='Create/modify ECS services')
@pass_context
def cli(ctx):
    if ctx.dry_run:
        ctx.warn_log("Running in dry run mode! Commands will not execute against AWS!")

    if ctx.env is "":
        ctx.env = click.prompt('In which environment would you like to deploy?', type=str)

    ecs_service = ECSService(env=ctx.env, profile=ctx.profile, config=ctx.config_file)
    ctx.ecs_service = ecs_service
    ctx.add_line_break()
    ctx.preamble_log("Current Env", ecs_service.get_env())
    ctx.preamble_log("Project Name", ecs_service.get_name())
    ctx.preamble_log("Service Name", ecs_service.get_service())
    ctx.preamble_log("Project Cluster", ecs_service.get_top_level_prop("cluster"))
    ctx.preamble_log("Project Family", ecs_service.get_top_level_prop("family"))
    ctx.add_line_break()

@cli.command(name = 'deploy-service', short_help='Creates or updates a service based off the deploy configuration file')
@pass_context
def deploy_service(ctx):
    ctx.info_log('Running deploy-service...')
    ctx.info_log('This command will create an ECS service or update an existing service.')
    service_exists = ctx.ecs_service.service_exists() # Does the service exist?
    if service_exists:
        if not ctx.dry_run:
            ctx.ecs_service.update_service()
        else:
            ctx.warn_log("Service exists but will not be updated due to dry run mode")
    else:
        if not ctx.dry_run:
            ctx.ecs_service.create_service()
        else:
            ctx.warn_log("Service does not exist but will not be created due to dry run mode")

@cli.command(name = 'register-task', short_help='Creates a task definition based off the deploy configuration file')
@pass_context
def register_task(ctx):
    ctx.info_log('Running register-task...')
    ctx.info_log('This command will create a task definition for project based off the deploy configuration file')
    ctx.add_line_break()
    task_definition = ctx.ecs_service.create_task_definition()
    if not ctx.dry_run:
        ctx.ecs_service.register_task_definition(task_definition)
    else:
        ctx.warn_log("Task not registered due to dry run flag")
        ctx.verbose_log("Generated task definition JSON:")
        ctx.verbose_log(json.dumps(task_definition))


@cli.command(name = 'build-image', short_help='Builds a Docker image and pushes to ECR based on your deploy configuration')
@pass_context
def buildImage(ctx):
    ctx.info_log("Running build-image...")
    ctx.info_log("This command will build the image for ")
    ctx.add_line_break()

    if not ctx.dry_run:
        built_tag = ctx.ecs_service.build_container_image()
        ctx.info_log("Built project image: " + built_tag)
    else:
        ctx.warn_log("Image not built due to dry run flag")
