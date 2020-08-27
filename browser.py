
nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

# write your code here
import sys, os, requests
from collections import deque
from colorama import Fore, Back, Style, init

from bs4 import BeautifulSoup

init()  # initialize colorama


args = sys.argv

# create directory if specified
if len(args) > 1:
    path = args[1]
    try:
        os.makedirs(path, exist_ok=True)
    except FileExistsError:
        print('Error: directory already exists')

page_stack = deque()  # stack for visited pages

while True:
    inp_str = input()
    if inp_str == 'exit':
        break
    if inp_str == 'back':  # show previous page, if it exists
        if len(page_stack) < 2:
            continue
        else:
            page_stack.pop()  # remove the current page from the stack
            page = globals()[page_stack[-1]]  # shows the previous page without removing it
            print(page)
            continue
    url = inp_str.strip().split('.')
    output_str = '_'.join(url[-2:])
    if len(url) < 2 or len(url) > 3:
        print('error')
    else:
        # save page url in the stack
        page_stack.append(output_str)
        if '//' not in url[0]:
            url[0] = 'https://' + url[0]
        site = '.'.join(url)
        r = requests.get(site)
        soup = BeautifulSoup(r.content, 'html.parser')
        links = soup.find_all('a')
        # print(links)
        # change color of the links to blue
        for link in links:
            if link.string:
                link.string = Fore.BLUE + link.string + Style.RESET_ALL
            # print(link.string)
        text = soup.get_text()
        print(text)
        # save page
        sitename = url[-2] if 'https://' not in url[-2] else url[-2][8:]
        filename = path + '\\' + sitename
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)

