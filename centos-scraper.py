from bs4 import BeautifulSoup
import requests
import csv


def make_list():
    url = "http://mirror.rise.ph/centos/7/"
    resource = requests.get(url)
    soup = BeautifulSoup(resource.text, 'html.parser')
    table = soup.find_all('tr')

    with open("output.csv", 'w+', newline='') as csvfile:
        fieldnames_csv = ['filename', 'download_link', 'size']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_csv)
        writer.writeheader()
        for root in table[3:-1]:

            recursive_folder(root, url, writer)


def recursive_folder(link, past, writer):
    """Accepts a link then recursively collect the files.
            Args:
                link : the needed data to be collected
                past : past version of the link
                writer : to be able to print to csv
    """
    test = link.a['href']
    print(test)
    if test.endswith('/'):
        resource = requests.get(past+test)
        past += test
        soup = BeautifulSoup(resource.text, 'html.parser')
        table = soup.find_all('tr')
        for root in table[3:-1]:
            recursive_folder(root,past,writer)

    else:
        to_split = link.text.split(" ", 3)
        filename = link.a['href']
        download_link = past+filename
        size = to_split[3]
        listu = {'filename': filename, 'download_link': download_link, 'size': size}
        writer.writerow(listu)

    return {}


def main():
    make_list()


if __name__ == '__main__':
    main()