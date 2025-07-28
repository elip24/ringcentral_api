from urllib.parse import urlencode

base_url = 'https://www.gibsondunn.com/people/?'

state_list = ['Century City', 'Dallas', 'Denver', 'Houston', 'Los Angeles', 'New York', 'Orange County', 'San Francisco', 'Washington DC']
practice_list = ['Projects', 'Real Estate']
industries_list = ['Data Centers and Digital Infrastructure']

def format_locations_param(locations: list[str]) -> str:
    cleaned_results = [parameter.replace(' ', '-').lower() for parameter in locations]
    return ','.join(cleaned_results)

def locations_with_parameters(base_url: str, state: str, parameter_list: list[str],second_parameter) -> list[str]:
    urls = []
    for parameter in parameter_list:
        cleaned_parameter = parameter.replace(' ', '-').lower()
        params = {
            "_people_location": state,
            second_parameter: cleaned_parameter
        }
        query_string = urlencode(params)
        full_url = f"{base_url}{query_string}"
        urls.append(full_url)

    return urls

state = format_locations_param(state_list)
practice_urls = locations_with_parameters(base_url=base_url, state=state, second_parameter='_people_practices',parameter_list=practice_list)
industry_urls=locations_with_parameters(base_url=base_url, state=state, second_parameter='_people_industries',parameter_list=industries_list)
joined_urls=practice_urls+industry_urls
for url in joined_urls:
    print(url)
