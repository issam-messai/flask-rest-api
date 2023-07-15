import logging
from flask import jsonify, request, g, Blueprint
from typing import Optional, Type

from flask_marshmallow import Schema
from marshmallow import EXCLUDE, ValidationError

from garden_api.common.exceptions import IdNotFoundException
from garden_api.models import db

class BaseApi():

    api_blueprint: Optional[Type[Blueprint]] = None
    model_DAO: Optional[Type[db.Model]] = None
    model_get_schema = None
    model_get_all_schema: Optional[Type[Schema]] = None
    model_post_schema : Optional[Type[Schema]] = None
    model_put_schema : Optional[Type[Schema]] = None
    update_command = None
    create_command = None
    DEFAULT_ERROR_MESSAGE ="Erreur de récupération dans la classe %s: %s"

    def __init_subclass__(cls) -> None:
        pass
    
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(type(self).__name__)
        
        @self.api_blueprint.route('/<int:id>', methods=['GET'])
        def get_by_id(id: int):
            try:
                model = self.model_DAO.get_by_id(id)
                result = self.model_get_schema.dump(model)
                if not result:
                    return self.no_item_found_response(id)
                return jsonify(result)
            except Exception as e:
                self.logger.error(
                    self.DEFAULT_ERROR_MESSAGE,
                    self.__class__.__name__,
                    str(e),
                    exc_info=True,
                )
                return self.response_500()

        @self.api_blueprint.route('/', methods=['GET'])
        def get_all():
            try:
                model_list = self.model_DAO.get_all()
                result = self.model_get_all_schema.dump(model_list)
                if not result:
                    return self.response_404()
                return jsonify(result)
            except Exception as e:
                self.logger.error(
                    self.DEFAULT_ERROR_MESSAGE,
                    self.__class__.__name__,
                    str(e),
                    exc_info=True,
                )
                return self.response_500()

        @self.api_blueprint.route('/<int:id>', methods=['PUT'])
        def update(id: int):
            try:
                item = self.model_put_schema.load(request.json, unknown=EXCLUDE)
            except ValidationError as error:
                return self.response_400(message=error.messages)
            try:
                updated_model = self.update_command(g.user, id, item).run()
                result = self.model_get_schema.dump(updated_model)
                return jsonify(result)
            except IdNotFoundException:
                return self.no_item_found_response(id)
            except ValidationError as e2:
                return self.response_400(message=e2.messages)
            except Exception as e:
                self.logger.error(
                    self.DEFAULT_ERROR_MESSAGE,
                    self.__class__.__name__,
                    str(e),
                    exc_info=True,
                )
                return self.response_500()

        @self.api_blueprint.route('/', methods=['POST'])
        def create():
            try:
                item = self.model_post_schema.load(request.json)
            # Validates schema
            except ValidationError as error:
                return self.response_400(message=error.messages)
            try:
                new_model = self.create_command(g.user, item).run()
                result = self.model_get_schema.dump(new_model)
                return jsonify(result)
            except ValidationError as err:
                return self.response_400(message=err.messages)
            except Exception as e:
                self.logger.error(
                    self.DEFAULT_ERROR_MESSAGE,
                    self.__class__.__name__,
                    str(e),
                    exc_info=True,
                )
                return self.response_500()

        @self.api_blueprint.route('/nombre', methods=['GET'])
        def get_count():
            try:
                result = self.model_DAO.get_count()
                if not result:
                    return self.response_404()
                return jsonify(result)
            except Exception as e:
                self.logger.error(
                    self.DEFAULT_ERROR_MESSAGE,
                    self.__class__.__name__,
                    str(e),
                    exc_info=True,
                )
                return self.response_500()

    @staticmethod
    def no_item_found_response(id):
        return jsonify('No item found with the given id: ' + str(id)), 404

    @staticmethod
    def response_500(message='internal server error'):
        return jsonify(message, 500)

    @staticmethod
    def response_404(message='not found'):
        return jsonify(message, 404)

    @staticmethod
    def response_400(message='bad request'):
        return jsonify(message, 400)