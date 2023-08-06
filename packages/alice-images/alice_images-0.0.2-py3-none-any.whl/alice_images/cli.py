import click

from . import alice_images_api as api


@click.group()
@click.option('--skill-id', prompt='Skill id', required=True, help='Alice skill id')
@click.option('--oauth-token', prompt='OAuth token', required=True, help='Account OAuth token')
@click.pass_context
def cli(ctx, skill_id, oauth_token):
    ctx.ensure_object(dict)

    ctx.obj.update({
        'skill_id': skill_id,
        'oauth_token': oauth_token,
    })


@cli.command('upload')
@click.option('--image-url', help='Image URL to upload.')
@click.option('--image-path', help='Image PATH to upload.')
@click.pass_context
def upload_image(ctx, image_url, image_path):
    kwargs = {
        'skill_id': ctx.obj['skill_id'],
        'oauth_token': ctx.obj['oauth_token']
    }

    if image_path:
        kwargs['image_path'] = image_path
    elif image_url:
        kwargs['image_url'] = image_url
    else:
        raise click.BadParameter('Need to provide image_url or image_path')

    click.echo(api.upload_image(**kwargs))


@cli.command('list')
@click.pass_context
def images_list(ctx):
    click.echo(api.uploaded_images_list(skill_id=ctx.obj['skill_id'], oauth_token=ctx.obj['oauth_token']))


@cli.command('status')
@click.pass_context
def free_space_status(ctx):
    click.echo(api.check_free_space(oauth_token=ctx.obj['oauth_token']))


@cli.command('delete')
@click.option('--image-id', required=True, help='Image ID to delete.')
@click.pass_context
def delete_image(ctx, image_id):
    click.echo(
        api.delete_uploaded_image(skill_id=ctx.obj['skill_id'], oauth_token=ctx.obj['oauth_token'], image_id=image_id)
    )


if __name__ == '__main__':
    cli()
