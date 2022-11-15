import requests
import json

from os import path
from pathlib import Path

from exceptions.PathNotExistError import PathNotExistError
from exceptions.PathNotFIleError import PathNotFileError
from exceptions.InvalidFileExtensionError import InvalidFileExtensionError
from exceptions.EmptyFileError import EmptyFileError
from exceptions.InvalidURLError import InvalidURLError
from exceptions.NoSearchResultsError import NoSearchResultsError

# Method 07.
# Creating a list of dictionaries,
# which every dictionary will keep the relevant data from the test results of each unique identifier.
# And if the data we are looking for does not appear in the results, the value of the data will be empty (e.g. 'score': '').
def get_uuid_information(uuid_list: list[str], url_result_api: str = 'https://urlscan.io/api/v1/result/', keys_list: list = ['url', 'time', 'screenshotURL', 'ips', 'certificates', 'score']):
    result_list_of_dictionaries: list[dict] = []

    for uuid in uuid_list:
        uuid_dictionary: dict = {}
        values_list: list = []
        key: int = 0
        response: requests.models.Response = requests.get(url_result_api + uuid)
        response_dictionary: dict = response.json()
        task: dict = response_dictionary['task']
        lists: dict = response_dictionary['lists']
        verdicts_urlscan: dict = response_dictionary['verdicts']['urlscan']

        if(task[keys_list[key]]):
            values_list.append(task[keys_list[key]])
            key += 1
        else:
            values_list.append('')
            key += 1
    
        if(task[keys_list[key]]):
            values_list.append(task[keys_list[key]])
            key += 1
        else:
            values_list.append('')
            key += 1
    
        if(task[keys_list[key]]):
            values_list.append(task[keys_list[key]])
            key += 1
        else:
            values_list.append('')
            key += 1

        if(lists[keys_list[key]]):
            values_list.append(lists[keys_list[key]])
            key += 1
        else:
            values_list.append('')
            key += 1

        if(lists[keys_list[key]]):
            values_list.append(lists[keys_list[key]])
            key += 1
        else:
            values_list.append('')
            key += 1

        if(verdicts_urlscan[keys_list[key]]):
            values_list.append(verdicts_urlscan[keys_list[key]])
            key += 1
        else:
            values_list.append('')
            key += 1

        uuid_dictionary = dict(zip(keys_list, values_list))
        result_list_of_dictionaries.append(uuid_dictionary)

    return result_list_of_dictionaries

# Method 06.
# Checks the contents of the file.
# The program will throw an error message (and stop the continuation of the process) in the following cases:
# 1. When the file is empty.
# 2. When the file contains invalid content.
# 3. When the file contains valid content but without any result in the search.

# If the content is valid and passed all the tests successfully,
# all uuids from the search results will be returned and stored in a list type variable.
def is_file_valid_content(file_path: str, mode: str = 'r', lines_counter: int = 0, url_search_api: str = 'https://urlscan.io/api/v1/search/?q=domain:', message_key: str = 'message', results_key: str = 'results', task_key: str = 'task', uuid_key: str = 'uuid'):
    uuid_list: list[str] = []

    file = open(file_path, mode)
    lines = file.readlines()
    file.close()

    if(len(lines) > lines_counter):

        for line in lines:
            lines_counter += 1
            response: requests.models.Response = requests.get(url_search_api + line)
            response_dictionary: dict = response.json()
            
            if(not(response_dictionary.get(message_key))):
                results: list[dict] = response_dictionary.get(results_key)
                results_length = len(results)

                if(results_length > 0):
                    
                    for result_index in range(results_length):
                        uuid_list.append(results[result_index][task_key][uuid_key])
                else:
                    raise NoSearchResultsError(lines_counter)
            else:
                raise InvalidURLError(lines_counter, response_dictionary.get(message_key))
    else:
        raise EmptyFileError(path.basename(file_path))

    return uuid_list

# Method 05.
# Checks if the path received from the user has a valid extension.
def is_path_valid_extension_file(file_path: str, valid_extension_file: str = '.txt'):

    if(not(Path(file_path).suffix == valid_extension_file)):
        raise InvalidFileExtensionError(Path(file_path).suffix)

# Methhod 04.
# Checks if the path received from the user is an object of type file in the operating system.
def is_path_file(file_path: str):

    if(not(path.isfile(file_path))):
        raise PathNotFileError(file_path)

# Method 03.
# Checks if the path received from the user exists in the operating system.
def is_path_exist(file_path: str):
    
    if(not(path.exists(file_path))):
        raise PathNotExistError(file_path)

# Method 02.
# A series of tests that verified that:
# 1. Does the path received from the user exist in the operating system?
# 2. Is the path received from the user an object of type file in the operating system?
# 3. If it is verified that the path received from the user is indeed a file,
# Is the file extension correct (should be .txt)?
# 4. Is the content of the file correct?

# If the file path has successfully passed all the validation tests, a list of the uuids received in the search is obtained.
def file_validation_tests(file_path: str, uuid_list: list[str] = []):
    is_path_exist(file_path)
    is_path_file(file_path)
    is_path_valid_extension_file(file_path)
    uuid_list = is_file_valid_content(file_path)

    return uuid_list

# Method 01.
# 1. The program receives input from the user.
# 2. The program will pass the user input to a series of validation tests.
# 3. The program will transfer a list of unique identifiers for the purpose of receiving relevant data obtained from the test results of each unique identifier.
# 4. The program will print the relevant data obtained in the test result of each unique identifier.
def scan_file(user_input_message: str = 'Enter the full path of the file you want to scan: '):
    uuid_list: list[str] = file_validation_tests(input(user_input_message))
    urls_results_list: list[dict] = get_uuid_information(uuid_list)

    pretty = json.dumps(urls_results_list, indent=4)

    print(pretty)

# ================================TESTS================================
scan_file()