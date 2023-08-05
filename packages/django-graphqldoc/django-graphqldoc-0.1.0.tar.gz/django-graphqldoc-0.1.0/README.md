# GraphQLDoc

GraphQLDoc is a simple Django app to document GraphQL schemas.

## Quick start
1. Add **graphqldoc** to your INSTALLED_APPS setting like this:
    
        INSTALLED_APPS = [
            ...
            'graphqldoc',
        ]

2. Add GRAPHQLDOC config settings in your settings file, and configure according to your needs, like this:

        GRAPHQLDOC = {
            'LOGO_URL': 'https://graphql.org/img/logo.svg',
            'TITLE': 'My GraphQL documentation',
        }
        
   This step is optional, it changes the logo and the default title in the template.

3. Include the graphqldoc URLconf in your project `urls.py` like this:

        path('docs/', include('graphqldoc.urls')),

4. Run `python manage.py migrate` to create the graphqldoc models.

5. Start the development server and visit http://localhost:8000/docs/ to view the rendered documentation for your GraphQL server.
