from multiprocessing import Pool
import bs4 as bs
import requests


urls = ['http://martinfowler.com', 'https://www.tutorialspoint.com']


def handle_local_links(url, link):
    print('Url:{}, Link {}'.format(url,link))
    if link.startswith('//'):
        return url
    elif link.startswith('/'):
        return ''.join([url, link])
    elif link.startswith('http'):
        return link
    elif link.startswith('#'):
        return ''
    else:
        return ''.join([url, link])


def get_links(url):
    try:
        print('Start parsing URL: {}'.format(url))
        response = requests.get(url)
        soup = bs.BeautifulSoup(response.text, 'lxml')
        body = soup.body
        links = [link.get('href') for link in body.find_all('a')]
        links = [handle_local_links(url, link) for link in links]
        # Encode
        links = [str(link.encode('ascii')) for link in links]
        return links
    except TypeError as type_error:
        # Iterate over None
        print (type_error)
        print ('Got a Type Error, probably a None that we tried to iterate')
        return []
    except IndexError as index_error:
        print (index_error)
        print ('We probably did not find any useful links, returning empty list')
        return []
    except AttributeError as attribute_error:
        print (attribute_error)
        print ('Probably we got None for links, so we return empty list')
        return []
    except Exception as exception:
        print (str(exception))
        return []


def main():
    how_many = 100
    p = Pool(processes=how_many)
    data = p.map(get_links, [link for link in urls])
    print ('Data after multiprocessing {}'.format(data))
    # data is now a list of lists
    # lets flatten it to a list
    data = [url for url_list in data for url in url_list]
    print ('Data is {}'.format(data))
    sorted_list = sorted(data)
    print ('Sorted List is {}'.format(sorted_list))
    p.close()
    with open('urls.txt', 'w') as f:
        f.write('\n'.join(sorted_list))


if __name__ == '__main__':
    main()
