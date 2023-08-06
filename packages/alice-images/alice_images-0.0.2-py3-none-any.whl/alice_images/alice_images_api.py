from typing import Union
from urllib.parse import urljoin

import requests


DIALOGS_HOST = 'https://dialogs.yandex.net'


def get_headers(oauth_token: str) -> dict:
    """Common headers for all requests"""
    return {
        'Authorization': f'OAuth {oauth_token}'
    }


def check_free_space(oauth_token: str, raw: bool = False) -> Union[dict, requests.Response]:
    """
    Check skill free space

    :param oauth_token: oauth token
    :param raw: return raw api response
    :return: uploaded image id or raw response
    """

    response = requests.get(
        url=urljoin(DIALOGS_HOST, '/api/v1/status'),
        headers=get_headers(oauth_token),
    )

    return response if raw else response.json()


def upload_image(skill_id: str, oauth_token: str, image_url: str = None, image_path: str = None,
                 raw: bool = False) -> Union[dict, requests.Response]:
    """
    Check skill free space

    :param skill_id: alice skill id
    :param oauth_token: oauth token
    :param image_url: image url to upload
    :param image_path: image local path to upload
    :param raw: return raw api response
    :return: uploaded image data id or raw response
    """
    url = urljoin(DIALOGS_HOST, f'/api/v1/skills/{skill_id}/images')
    headers = get_headers(oauth_token)

    if image_url:
        response = requests.post(url=url, headers=headers, json={'url': image_url})
    elif image_path:
        response = requests.post(url=url, headers=headers, files={'file': open(image_path, 'rb')})
    else:
        raise Exception('Need to provide image_url or image_path')

    return response if raw else response.json()


def uploaded_images_list(skill_id: str, oauth_token: str, raw: bool = False) -> Union[dict, requests.Response]:
    """
    Get uploaded skill images

    :param skill_id: alice skill id
    :param oauth_token: oauth token
    :param raw: return raw api response
    :return: uploaded image id or raw response
    """

    response = requests.get(
        url=urljoin(DIALOGS_HOST, f'/api/v1/skills/{skill_id}/images'),
        headers=get_headers(oauth_token),
    )

    return response if raw else response.json()


def delete_uploaded_image(skill_id: str, oauth_token: str, image_id: str,
                          raw: bool = False) -> Union[dict, requests.Response]:
    """
    Delete uploaded image

    :param skill_id: alice skill id
    :param oauth_token: oauth token
    :param image_id: image id to delete
    :param raw: return raw api response
    :return: uploaded image id or raw response
    """

    response = requests.delete(
        url=urljoin(DIALOGS_HOST, f'/api/v1/skills/{skill_id}/images/{image_id}/'),
        headers=get_headers(oauth_token),
    )

    return response if raw else response.json()
