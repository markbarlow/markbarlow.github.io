# Generate simple e-learning courses

- course-template.html — pure renderer, no data
- example-course.yaml — "Coffee Brewing" sample covering every content type used in the template
- example-course.html — example of the built output from the yaml file, immediately viewable
- build.py — the script which converts the yaml into course content using the template and outputting a self-contained course file. Usage: python3 build.py your-course.yaml output.html

Progress is stored using localStorage

