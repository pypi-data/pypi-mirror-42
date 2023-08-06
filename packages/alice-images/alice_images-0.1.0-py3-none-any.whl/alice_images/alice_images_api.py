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


def upload_image(skill_id: str, oauth_token: str, image_path_or_url: str = None,
                 raw: bool = False) -> Union[dict, requests.Response]:
    """
    Check skill free space

    :param skill_id: alice skill id
    :param oauth_token: oauth token
    :param image_path_or_url: image file path or url to upload
    :param raw: return raw api response
    :return: uploaded image data id or raw response
    """
    url = urljoin(DIALOGS_HOST, f'/api/v1/skills/{skill_id}/images')
    headers = get_headers(oauth_token)

    if image_path_or_url.startswith('http'):
        response = requests.post(url=url, headers=headers, json={'url': image_path_or_url})
    else:
        response = requests.post(url=url, headers=headers, files={'file': open(image_path_or_url, 'rb')})

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
