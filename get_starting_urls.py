from urllib.parse import urlencode

base_url = 'https://www.gibsondunn.com/people/?'

state_list = ['Century City', 'Dallas', 'Denver', 'Houston', 'Los Angeles', 'New York', 'Orange County', 'San Francisco', 'Washington DC']
practice_list = ['Projects', 'Real Estate']
industries_list = ['Data Centers and Digital Infrastructure']

def format_locations_param(locations: list[str]) -> str:
    cleaned_results = [parameter.replace(' ', '-').lower() for parameter in locations]
    return ','.join(cleaned_results)

def locations_with_parameters(base_url: str, state: str, practices: list[str]) -> list[str]:
    urls = []
    for practice in practices:
        cleaned_practice = practice.replace(' ', '-').lower()
        params = {
            "_people_location": state,
            "_people_practices": cleaned_practice
        }
        query_string = urlencode(params)
        full_url = f"{base_url}{query_string}"
        urls.append(full_url)
    return urls

def locations_with_industries(base_url: str, state: str, industries: list[str]) -> list[str]:
    urls = []
    for industry in industries:
        cleaned_industry = industry.replace(' ', '-').lower()
        params = {
            "_people_location": state,
            "_people_industries": cleaned_industry
        }
        query_string = urlencode(params)
        full_url = f"{base_url}{query_string}"
        urls.append(full_url)
    return urls


state = format_locations_param(state_list)
practice_urls = locations_with_parameters(base_url=base_url, state=state, practices=practice_list)
industry_urls = locations_with_industries(base_url=base_url, state=state, industries=industries_list)

all_urls = practice_urls + industry_urls
for url in all_urls:
    print(url)
