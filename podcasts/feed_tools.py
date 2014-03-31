from bs4 import BeautifulSoup
from dateutil import parser
import feedparser
from urllib.error import HTTPError
from urllib.request import urlopen


def get_podcast_data(feed_url):
    try:
        feed_request = urlopen(feed_url)
    except HTTPError as e:
        raise e

    feed_xml = feed_request.read()

    feed = feedparser.parse(feed_xml).feed
    soup = BeautifulSoup(feed_xml)
    try:
        title = feed.title
    except AttributeError:
        raise AttributeError('xml')
    response = {
        'title': title,
        'description': feed.subtitle,
        'link': getattr(feed, 'link', ""),
        'language': __get_language(feed),
        'tags': __get_tags(feed),
        'images': __get_images(soup, feed),
        'categories': __get_categories(soup),
    }
    return response


def __get_language(feed):
    return feed.language[:2]


def __get_categories(soup):
    categories = {}
    for each in soup.find_all('itunes:category'):
        category = each['text']
        subcategories = []
        for each in each.find_all('itunes:category'):
            subcategory = each['text']
            subcategories.append(subcategory)
        categories.update({category: subcategories})
    return categories


def __get_tags(feed):
    try:
        return [tag.term for tag in feed.tags]
    except AttributeError:
        return []


def __get_images(soup, feed):
    images = []
    # Find an itunes:image inside the channel
    itunes_image = soup.channel.find('itunes:image', recursive=False)
    if itunes_image:
        href = itunes_image.get('href')
        if href and href not in images:
            images.append(href)
    # Find an image element that's a direct child to the channel element
    image_tag = soup.channel.find('image', recurisve=False)
    if image_tag:
        url = getattr(getattr(image_tag, 'url', None), 'text', None)
        if url:
            images.append(url)
    # Lastly add feedparser's image if it isn't already in the list
    feedparser_image = getattr(getattr(feed, 'image', None), 'href', None)
    if feedparser_image and feedparser_image not in images:
        images.append(feedparser_image)
    return images


def get_episode_data(feed_url, existing_episode_titles):
    feed = feedparser.parse(feed_url)
    episodes = []
    for feed_episode in feed.entries:
        try:
            if feed_episode.title in existing_episode_titles:
                # If the episode already is in the DB
                continue
        except AttributeError:
            # The episode in the feed doesn't have a title
            continue
        episodes.append({
            'title': feed_episode.title,
            'link': __get_link(feed_episode),
            'description': __get_description(feed_episode),
            'published': __get_published(feed_episode),
            'audio_file': __get_audio_file(feed_episode),
        })
    return episodes


def __get_link(episode):
    return getattr(episode, 'link', '')


def __get_published(episode):
    # parser.parse(): http://stackoverflow.com/a/18726020/595990
    return parser.parse(episode.published)


def __get_audio_file(episode):
    enclosures = getattr(episode, 'enclosures', '')
    for enclosure in enclosures:
        if enclosure.type[:5] == 'audio':
            return enclosures[0].href
    return ''


def __get_description(episode):
    summary = getattr(episode, 'summary', None)
    if summary:
        return summary
    content = getattr(episode, 'content', None)
    if content:
        return content[0].value
    return ''
