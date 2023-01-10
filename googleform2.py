from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Replace form_id with the ID of the form you want to fill
form_id = '1FAIpQLScvKGo6JBfGUd7R0vHBdw04n93e4mEffkgtApM-sThmstvZdA'

try:
    # Create a service object
    service = build('forms', 'v1', credentials=credentials)

    # Get the form
    form = service.forms().get(formId=form_id).execute()

    # Print the form's title
    print(form['title'])

    # Set the form responses
    form_response = {
        'responses': [{
            'itemId': item['id'],
            'choiceResponse': {
                'response': 'Option 1'
            }
        } for item in form['items']]
    }

    # Submit the form response
    response = service.forms().response().create(formId=form_id, body=form_response).execute()

    print(f'Response ID: {response["responseId"]}')

except HttpError as error:
    print(f'An error occurred: {error}')
