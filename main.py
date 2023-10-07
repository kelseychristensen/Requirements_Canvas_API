import requests


# PRINTS API RESPONSE CODE
def print_api_response(response, name):
    if response.status_code == 200:
        print(f"{name} updated successfully!\n")
    else:
        print("Failed to update module item. Status code:", response.status_code)
        print("Response:", response.text)


# RETURNS JSON OF MODULES IN A COURSE
def get_modules(course_id, headers, url):
    response = requests.get(url=f"{url}/courses/{course_id}/modules?per_page=100", headers=headers)
    all_modules = response.json()
    modules = [module for module in all_modules if module["published"]]
    return modules


# RETURNS JSON OF MODULES ITEMS IN A MODULE
def get_modules_items(course_id, module_id, headers, url):
    response = requests.get(url=f"{url}/courses/{course_id}/modules/{module_id}/items?per_page=100", headers=headers)
    module_items = response.json()
    published_items = [item for item in module_items if item["published"]]
    return published_items


# ADDS COMPLETION REQUIREMENTS TO ALL MODULES ITEMS IN A MODULE
def add_completion_requirements(course_id, module_id, headers, url):
    module_items = get_modules_items(course_id, module_id, headers, url)
    for module_item in module_items:
        item_id = module_item["id"]
        item_type = module_item["type"]
        name = module_item["title"]
        print(f"Updating Module Item {item_type}: {name}")
        if item_type == "Assignment" or item_type == "Quiz":
            data = {"module_item[completion_requirement][type]": "must_submit"}
        elif item_type == "Discussion":
            data = {"module_item[completion_requirement][type]": "must_contribute"}
        else:
            data = {"module_item[completion_requirement][type]": "must_view"}
        response = requests.put(url=f"{url}/courses/{course_id}/modules/{module_id}/items/{item_id}",
                                headers=headers, data=data)
        print_api_response(response, name)


# ADDS PRE-REQUISITES TO A MODULE
def add_prereq(course_id, headers, modules, module, module_name, module_id, previous_module, url):
    current_index = modules.index(module)
    print(f"Updating Module {current_index + 1}\n")
    data = {
        "module[name]": module_name,
        "module[prerequisite_module_ids][]": previous_module["id"]}
    response = requests.put(url=f"{url}/courses/{course_id}/modules/{module_id}?per_page=100",
                            headers=headers, data=data)
    print_api_response(response, module_name+" Pre-Reqs")


def add_sequential_progress(course_id, headers, module_name, module_id, url):
    data = {"module[name]": module_name,
            "module[require_sequential_progress]": "true"}
    response = requests.put(url=f"{url}/courses/{course_id}/modules/{module_id}?per_page=100",
                            headers=headers, data=data)
    print_api_response(response, module_name+" Sequential Progress")


# ADDS ALL MODULE ITEM REQUIREMENTS AND PRE-REQUISITES NEEDED IN A COURSE
def add_prereqs_and_reqs(course_id, headers, url):
    all_modules = get_modules(course_id, headers, url)
    for module in all_modules:
        current_index = all_modules.index(module)
        current_name = module['name']

        current_id = module["id"]
        previous_module = all_modules[current_index - 1]

        add_prereq(course_id, headers, all_modules, module, current_name, current_id, previous_module, url)
        add_completion_requirements(course_id, current_id, headers, url)
        add_sequential_progress(course_id, headers, current_name, current_id, url)


def run():
    instance = input("What is your instance name? Example: [INSTANCE].instructure.com when you login.\n")
    beta_or_prod_input = input("Are you working in the beta instance? (Y/N)\n")
    if beta_or_prod_input.lower() == "y":
        url = f"https://{instance}.beta.instructure.com/api/v1"
    else:
        url = f"https://{instance}.instructure.com/api/v1"

    token = input("Please enter your API token.\n")
    headers = {
        "authorization": f"Bearer {token}"}

    user_input = input("What is the Course ID of the course that needs requirements?\n"
                       "If there are multiple, please enter them as a comma-separated list.\n")

    for course in user_input.split(", "):
        print(f"Updating Course # {course}\n")
        add_prereqs_and_reqs(course, headers, url)

        print(f"All requirements have been added to Course # {course}!\n")

    print(f"All requirements across all courses have been added!")


run()
