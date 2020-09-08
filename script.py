from bot import TemplateBot
from bs4 import BeautifulSoup
import xlsxwriter
# pip install -r requirements.txt

class FacebookParser(TemplateBot):
    path_to_login = '//*[@id="mobile_login_bar"]/div[2]/a[1]'
    path_to_login_input = '//*[@id="m_login_email"]'
    path_to_password_input = '//*[@id="m_login_password"]'
    path_to_login_button = '//*[@id="u_0_4"]/button'
    TIME_TO_SCROLL = 600

    def parse(self, group_id: str = None) -> list: # 1643910255830661
        self.driver.get(f'https://m.facebook.com/groups/{group_id}#_=_')
        self.driver.find_element_by_xpath(self.path_to_login).click()
        self.driver.find_element_by_xpath(self.path_to_login_input).send_keys(self.username)
        self.driver.find_element_by_xpath(self.path_to_password_input).send_keys(self.password)
        self.protected_sleep(3.12345678876543234567898765434567890987654)
        self.driver.find_element_by_xpath(self.path_to_login_button).click()
        self.protected_sleep(5.2345678765432345678765434567876543)

        for _ in range(self.TIME_TO_SCROLL):
            self.driver.execute_script('scrollTo(0, 1000000000000000)')
            self.protected_sleep(3.5765456789098765456789098765)

        html = BeautifulSoup(self.driver.page_source, 'html.parser')
        posts = html.select('#m_group_stories_container')[0]
        self.driver.close()
        results = []

        for post in posts.find_all('div', {'class': 'story_body_container'}):
            try:
                author = post.find('h3', {'class': '_52jd _52jb _52jh _5qc3 _4vc- _3rc4 _4vc-'}).find('a').text
                date = post.find('div', {'class': '_52jc _5qc4 _78cz _24u0 _36xo'}).find('abbr').text
                description = post.find('div', {'class': '_5rgt _5nk5 _5msi'}).text
                try:
                    image = post.find('div', {'class': '_5uso _5t8z'}).find('a').get('href')
                    # https://m.facebook.com/
                except:
                    image = None
                
                results.append({
                    'author': author,
                    'date': date,
                    'description': description,
                    'image': ('https://m.facebook.com' + image) if image else None
                })
            
            except:
                pass
        
        return results

if __name__ == "__main__":
    login = '<phone or gmail>'
    password = 'password'

    parser = FacebookParser(show = True)
    parser.login(login, password)
    data = parser.parse('1643910255830661') # group id

    workbook = xlsxwriter.Workbook('posts.xlsx') 
    worksheet = workbook.add_worksheet()

    row, column = 0, 0
    titles = ['Author', 'Date', 'Description', 'Image']

    for item in titles: 
        worksheet.write(row, column, item) 
        column += 1

    row += 1

    for item in data:
        worksheet.write(row, 0, item['author']) 
        worksheet.write(row, 1, item['date']) 
        worksheet.write(row, 2, item['description']) 
        worksheet.write(row, 3, item['image']) 

        row += 1

    workbook.close()
    print(len(data))
