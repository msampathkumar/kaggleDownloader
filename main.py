"""To Download competetion files from Kaggle.

TODO:

* To give competetion with out `-`, we currently depend on it.
* To micro mise the jobs here
* To re-check the argument input style
    * clear any trailing space/arg parse takes care of
* To include search of competetion


Long Terms Goals:

* To make interactive search after connecting to kaggle
* To create a new folder & store data there.
* Download all file or only some? with yes or no
    * commit or RE-DO - selecting files
"""
from robobrowser import RoboBrowser
import argparse


def main(competition, username, password):
    """To login and download files."""
    browser = RoboBrowser(history=True, parser="html.parser")
    base = 'https://www.kaggle.com'
    browser.open('/'.join([base, 'account/login']))

    login_form = browser.get_form(action='/account/login')
    login_form['UserName'] = username
    login_form['Password'] = password
    browser.submit_form(login_form)

    browser.open('/'.join([base, 'c', competition, 'data']))
    files = []
    for a_href in browser.get_links():
        if '.zip' in a_href.text:
            files.append(a_href)

    print('...downloading {0} files...'.format(len(files)))
    for f in files:
        request = browser.session.get(base + f.attrs['href'], stream=True)
        with open(f.attrs['name'], "wb") as zip_file:
            zip_file.write(request.content)


def run():
    """To take commandlien Arguments."""
    parser = argparse.ArgumentParser(
        description='download kaggle datasets')
    parser.add_argument('-u', '--username', help='kaggle username')
    parser.add_argument('-p', '--password', help='kaggle password')
    parser.add_argument('-c', '--competition', help='competition url')
    args = parser.parse_args()

    main(competition=args.competition,
         username=args.username, password=args.password)

if __name__ == '__main__':
    run()
