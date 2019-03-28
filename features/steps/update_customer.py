from behave import when, then

@when('I update the name of customer with an id of "{id}" to "{name}"')
def update_customer(context, id, name):
    (first_name, surname) = name.split(' ', 2)
    response = context.web_client.put(
        f'/customers/{id}',
        json={'firstName': first_name, 'surname': surname})

    assert response.status_code == 200, response.status_code
    context.customer_id = response.get_json()['customerId']

