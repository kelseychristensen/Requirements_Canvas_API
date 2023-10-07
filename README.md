<h1 align="center">Python Script to Add Requirements through Canvas API</h1>

<p align="center">
This is a Python script that will update the requirements for a 
given Canvas course ID or set of Canvas course IDs so that 
A) modules and module items must be completed in sequential order (meaning each module bears a 
pre-requisite of the previous module and module items must be completed
in sequential order), and B) module items which can be submitted (e.g.
discussions, quizzes, assignments) <i>must</i> be submitted while all
other item types must be viewed. 

This script does the following: 

- Asks the user the for their instance name, their API token (generated in Canvas User settings), and whether they are working in the beta or production instance (you could augment the code to store your instance name and token as a variable). 
- Asks the user for a course ID or comma-separated list of course IDs. 
- Gets all the modules IDs in the current course ID and iterates through them.
- For each module ID in a given course ID, it:
  - Sets "module[require_sequential_progress]" to true, requiring that module items be completed in sequential order.
  - Determines if a module is the first module in a course; if it is not, it sets the _previous_ module as a prerequisite.
  - Gets all the module item IDs and iterates through them. 
  - For each module item in a module, it: 
    - Determines the module type 
    - If the module item type is a quiz, assignment, or discussion, it sets the completion requirement to "must submit"
    - If the module item type is _not_ a quiz, assignment, or discussion, it sets the completion requirement to "must view."
- The code will only affect published modules (requiring the completion of assigments in an unpublished module or making an unpublished module a pre-requisite will make a student unable to continue.)
- When the code has run, all published modules will: 
  - Bear a pre-requisite which is the previous module. 
  - Require the completion of each module item (quiz, page, assignment).
  - Require sequential progress of module items. 

## Links

- [Repo](https://github.com/kelseychristensen/Requirements-Canvas-API "to-do-tool")

## Screenshots

#### Console Feedback at Start
![Start](at start.PNG "at start")
#### Console Feedback During Run
![Run](middle.PNG "at start")
#### Console Feedback at Completion
![End](end.PNG "at end")


### Built with

- Python
- Canvas REST API

### Resources

Relevant docs: https://canvas.instructure.com/doc/api/modules.html

### Continued development

This could be improved with a graphic user interface that a layman could use.


```python
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
```

## Author

Kelsey Christensen

- [Profile](https://github.com/kelseychristensen "GitHub")
- [Email](mailto:kelsey.c.christensen@gmail.com?subject=Hi "Email")
- [Dribble](https://dribbble.com/kelseychristensen "Dribble")
- [Website](http://kelseychristensen.com/ "Website")