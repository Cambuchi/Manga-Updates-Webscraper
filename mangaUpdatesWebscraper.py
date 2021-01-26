#!/usr/bin/env python3

# mangaUpdates.py - script that scrapes information on mangas from mangaupdates.com and writes
# the data into a csv file. Dependent on requests and bs4.

import requests
import logging
import re
import time
import csv
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
logging.disable(logging.DEBUG) # un/comment to un/block debug log messages
logging.disable(logging.INFO) # un/comment to un/block info log messages


def get_soup(url):
    """ Create a soup object with the provided URL. """
    logging.info(f'Creating soup for {url}...')

    res = requests.get(url)
    res.raise_for_status()
    manga_soup = BeautifulSoup(res.content, 'html.parser')
    logging.info('Soup created successfully, returning soup object.')
    return manga_soup


def parse_soup(soup):
    """ Parse the soup object created with beautiful soup into a dictionary. """
    logging.info('Parsing information from provided soup object...')
    output_dict = {}

    title = soup.select('.releasestitle.tabletitle')[0].text
    output_dict['title'] = title
    logging.debug(f'title is: {title}')

    description = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                              'div:nth-child(3) > div:nth-child(2)')[0].text
    description_pattern = r'.*[\.{3}]?'
    description = description.strip()
    description_regex = re.search(description_pattern, description)
    output_dict['description'] = description_regex[0]
    logging.debug(f'description is: {description_regex[0]}')

    media_type = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                             'div:nth-child(3) > div:nth-child(5)')[0].text
    output_dict['media_type'] = media_type.strip()
    logging.debug(f'media_type is: {media_type.strip()}')

    status = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                         'div:nth-child(3) > div:nth-child(20)')[0].text
    output_dict['status'] = status.strip()
    logging.debug(f'status is: {status.strip()}')

    authors = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                          'div:nth-child(4) > div:nth-child(17)')[0].text
    output_dict['authors'] = authors.strip()
    logging.debug(f'authors is: {authors.strip()}')

    artists = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                          'div:nth-child(4) > div:nth-child(20)')[0].text
    output_dict['artists'] = artists.strip()
    logging.debug(f'artists is: {artists.strip()}')

    year = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                       'div:nth-child(4) > div:nth-child(23)')[0].text
    output_dict['year'] = year.strip()
    logging.debug(f'year is: {year.strip()}')

    original_publisher = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                     'div:nth-child(4) > div:nth-child(26)')[0].text
    output_dict['original_publisher'] = original_publisher.strip()
    logging.debug(f'original_publisher is: {original_publisher.strip()}')

    user_rating = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                              'div:nth-child(3) > div:nth-child(35)')[0].text
    user_pattern = r'Average: (\d?\d?[.]?\d?\d).*\((\d+).*Average: (\d?\d?[.]?\d?\d)'
    user_rating = user_rating.replace("&nbsp;", "")
    user_rating_regex = re.findall(user_pattern, user_rating)

    average = user_rating_regex[0][0]
    output_dict['average'] = average
    logging.debug(f'average is: {average}')

    total_votes = user_rating_regex[0][1]
    output_dict['total_votes'] = total_votes
    logging.debug(f'total_votes is: {total_votes}')

    bay_average = user_rating_regex[0][2]
    output_dict['bay_average'] = bay_average
    logging.debug(f'bay_average is: {bay_average}')

    licensed_english = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                   'div:nth-child(4) > div:nth-child(32)')[0].text
    output_dict['licensed_english'] = licensed_english.strip()
    logging.debug(f'licensed_english is: {licensed_english.strip()}')

    weekly_position = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                  'div:nth-child(4) > div:nth-child(38) > b:nth-child(2)')[0].text
    output_dict['weekly_position'] = weekly_position
    logging.debug(f'weekly_position is: {weekly_position}')

    monthly_position = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                   'div:nth-child(4) > div:nth-child(38) > b:nth-child(6)')[0].text
    output_dict['monthly_position'] = monthly_position
    logging.debug(f'monthly_position is: {monthly_position}')

    three_month_position = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                       'div:nth-child(4) > div:nth-child(38) > b:nth-child(10)')[0].text
    output_dict['three_month_position'] = three_month_position
    logging.debug(f'three_month_position is: {three_month_position}')

    six_month_position = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                     'div:nth-child(4) > div:nth-child(38) > b:nth-child(14)')[0].text
    output_dict['six_month_position'] = six_month_position
    logging.debug(f'six_month_position is: {six_month_position}')

    yearly_position = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                  'div:nth-child(4) > div:nth-child(38) > b:nth-child(18)')[0].text
    output_dict['yearly_position'] = yearly_position
    logging.debug(f'yearly_position is: {yearly_position}')

    percent_ten = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                              'div:nth-child(3) > div:nth-child(35) > div:nth-child(5) > '
                              'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_ten'] = percent_ten.strip()
    logging.debug(f'percent_ten is: {percent_ten.strip()}')

    percent_nine_plus = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                    'div:nth-child(3) > div:nth-child(35) > div:nth-child(6) > '
                                    'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_nine_plus'] = percent_nine_plus.strip()
    logging.debug(f'percent_nine_plus is: {percent_nine_plus.strip()}')

    percent_eight_plus = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                     'div:nth-child(3) > div:nth-child(35) > div:nth-child(7) > '
                                     'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_eight_plus'] = percent_eight_plus.strip()
    logging.debug(f'percent_eight_plus is: {percent_eight_plus.strip()}')

    percent_seven_plus = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                     'div:nth-child(3) > div:nth-child(35) > div:nth-child(8) > '
                                     'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_seven_plus'] = percent_seven_plus.strip()
    logging.debug(f'percent_seven_plus is: {percent_seven_plus.strip()}')

    percent_six_plus = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                   'div:nth-child(3) > div:nth-child(35) > div:nth-child(9) > '
                                   'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_six_plus'] = percent_six_plus.strip()
    logging.debug(f'percent_six_plus is: {percent_six_plus.strip()}')

    percent_five_plus = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                    'div:nth-child(3) > div:nth-child(35) > div:nth-child(10) > '
                                    'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_five_plus'] = percent_five_plus.strip()
    logging.debug(f'percent_five_plus is: {percent_five_plus.strip()}')

    percent_four_plus = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                    'div:nth-child(3) > div:nth-child(35) > div:nth-child(11) > '
                                    'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_four_plus'] = percent_four_plus.strip()
    logging.debug(f'percent_four_plus is: {percent_four_plus.strip()}')

    percent_three_plus = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                     'div:nth-child(3) > div:nth-child(35) > div:nth-child(12) > '
                                     'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_three_plus'] = percent_three_plus.strip()
    logging.debug(f'percent_three_plus is: {percent_three_plus.strip()}')

    percent_two_plus = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                   'div:nth-child(3) > div:nth-child(35) > div:nth-child(13) > '
                                   'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_two_plus'] = percent_two_plus.strip()
    logging.debug(f'percent_two_plus is: {percent_two_plus.strip()}')

    percent_one_plus = soup.select('#main_content > div:nth-child(2) > div.row.no-gutters > '
                                   'div:nth-child(3) > div:nth-child(35) > div:nth-child(14) > '
                                   'div.col-2.col-sm-2.text.text-right')[0].text.strip('%')
    output_dict['percent_one_plus'] = percent_one_plus.strip()
    logging.debug(f'percent_one_plus is: {percent_one_plus.strip()}')

    logging.info('All information has been parsed, returning output_dict.')
    return output_dict


def main():
    """ Writes data from a dictionary into a csv file. Establishes fieldnames for dictionary values. Increments
        ID of manga titles to the provided number, as of 2021, highest manga ID is 176901, so any value higher
        that also raises an IndexError means the web-scraper has reached the end. """
    home_url = 'https://www.mangaupdates.com/series.html?id='
    manga_id = 1
    fieldnames = ['title', 'description', 'media_type', 'status', 'authors', 'artists', 'year', 'original_publisher',
                  'average', 'total_votes', 'bay_average', 'licensed_english', 'weekly_position', 'monthly_position',
                  'three_month_position', 'six_month_position', 'yearly_position', 'percent_ten', 'percent_nine_plus',
                  'percent_eight_plus', 'percent_seven_plus', 'percent_six_plus', 'percent_five_plus',
                  'percent_four_plus', 'percent_three_plus', 'percent_two_plus', 'percent_one_plus']

    with open('manga_updates_info.csv', 'w', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        while manga_id <= 10:  # Change the value here to scrape more than 10 mangas
            try:
                writer.writerow(parse_soup(get_soup(home_url  + str(manga_id))))
                manga_id += 1
                time.sleep(1)
            except IndexError:
                print('There was an IndexError.')
                if manga_id > 176901:
                    print('No more mangas to scrape.')
                    break
                else:
                    manga_id += 1
                    continue


if __name__ == '__main__':
    main()
