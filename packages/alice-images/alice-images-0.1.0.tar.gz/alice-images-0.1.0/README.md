# Alice-images

Work with alice skills images: upload|list|delete

[Yandex docs](https://tech.yandex.ru/dialogs/alice/doc/resource-upload-docpage/)


### Usage

#### In code

    from alice_images import upload_image

    upload_image(
        skill_id='<skill_id>',
        oauth_token='<oauth_token>',
        image='https://<image_url>/'  # or path '/tmp/image.jpg'
    )
    
#### CLI

Upload by url:

    alice_images --skill_id '<skill_id>' --oauth_token '<oauth_token>' upload 'https://<image_url>/'

Upload by path:

    alice_images --skill_id '<skill_id>' --oauth_token '<oauth_token>' upload '/tmp/image.jpg'
    
For more info use `--help`:

    $ alice_images --help
    Usage: alice_images [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --skill-id TEXT     Alice skill id  [required]
      --oauth-token TEXT  Account OAuth token  [required]
      --help              Show this message and exit.
    
    Commands:
      delete
      list
      status
      upload
