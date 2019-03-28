from http import HTTPStatus

from flask import jsonify, Blueprint, current_app, request
from schema import Schema, SchemaError, And

from customer_service.model import commands
from customer_service.model.customer import Customer
from customer_service.model.errors import CustomerNotFound

customers = Blueprint('customers', __name__, url_prefix='/customers/')

CREATE_PAYLOAD_SCHEMA = Schema({"firstName": And(str, len),
                                "surname": And(str, len)})


@customers.route('/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer_repository = current_app.customer_repository

    customer = commands.get_customer(
        customer_id=int(customer_id),
        customer_repository=customer_repository)

    return jsonify(customerId=str(customer.customer_id),
                   firstName=customer.first_name,
                   surname=customer.surname)


@customers.route('/', methods=['POST'])
def create_customer():
    customer_repository = current_app.customer_repository

    if not request.is_json:
        raise ContentTypeError()

    body = request.get_json()

    CREATE_PAYLOAD_SCHEMA.validate(body)

    customer = Customer(first_name=body['firstName'],
                        surname=body['surname'])

    commands.create_customer(
        customer=customer,
        customer_repository=customer_repository)

    return jsonify(customerId=str(customer.customer_id),
                   firstName=customer.first_name,
                   surname=customer.surname), HTTPStatus.CREATED


@customers.route('/<string:customer_id>', methods=['PUT'])
def update_surname(customer_id):
    customer_repository = current_app.customer_repository

    if not request.is_json:
        raise ContentTypeError()

    body = request.get_json()

    commands.update_customer_surname(int(customer_id), body['surname'], customer_repository)

    return jsonify(customerId=str(customer_id)), HTTPStatus.OK


@customers.errorhandler(CustomerNotFound)
def customer_not_found(e):
    return jsonify(dict(message='Customer not found')), HTTPStatus.NOT_FOUND


@customers.errorhandler(SchemaError)
def invalid_schema(e):
    return jsonify(dict(message=str(e))), HTTPStatus.BAD_REQUEST


class ContentTypeError(RuntimeError):
    pass


@customers.errorhandler(ContentTypeError)
def content_type_error(e):
    return jsonify(dict(message='Request must be application/json')), \
           HTTPStatus.UNSUPPORTED_MEDIA_TYPE





def thing_to_call():
    return 'real value'


def thing_to_test(value):
    return thing_to_call(str(value))
