from behave import when, then


@when('I create customer "{name}"')
def create_customer(context, name):
    (first_name, surname) = name.split(' ', 2)
    response = context.web_client.post(
        '/customers/',
        json={'firstName': first_name, 'surname': surname})

    assert response.status_code == 201, response.status_code
    context.customer_id = response.get_json()['customerId']


@then('I should be able to fetch customer details for "{name}"')
def fetch_customer_by_context_id(context, name):
    response = context.web_client.get(f'/customers/{context.customer_id}')

    assert response.status_code == 200, response.status_code
    customer = response.get_json()
    name_to_check = f"{customer['firstName']} {customer['surname']}"
    assert name_to_check == name, name_to_check
