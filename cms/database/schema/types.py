__author__ = 'Gareth Coles'


class Schema(object):
    #: :type: dict
    schema = None

    def __init__(self, schema):
        """
        :type schema: dict
        """

        self.schema = schema

    def validate(self, data):
        return False


class TypeAndMembershipCheckingSchema(Schema):
    """
    Validates data against a schema, checking for both membership and type

    This will fail in the following situations:
    * If a key is in the data but not in the schema
    * If a key is in the schema but not in the data, and the schema doesn't
      allow None as a type for that data value
    * If a key is in both the data and schema, but the schema doesn't have a
      matching type for the data value
    """

    def validate(self, data):
        """
        Validates a data dictionary against the stored schema dictionary

        :param data: The data to check
        :type data: dict

        :return: True if the data validates, False otherwise
        :rtype: bool
        """

        for key, value in data.iteritems():
            if key in self.schema:
                types = self.schema.get(key)

                if isinstance(types, list):
                    for t in types:
                        if not isinstance(value, t):
                            return False
                else:
                    if not isinstance(value, types):
                        return False
            else:
                return False

        for key, value in self.schema.iteritems():
            if key not in data:
                if isinstance(value, list):
                    if None not in value:
                        return False
                else:
                    if value is not None:
                        return False


class TypeCheckingSchema(Schema):
    """
    Validates data against a schema, checking only for type

    This will fail in the following situations:
    * If a key is in both the data and schema, but the schema doesn't have a
      matching type for the data value
    """

    def validate(self, data):
        """
        Validates a data dictionary against the stored schema dictionary

        :param data: The data to check
        :type data: dict

        :return: True if the data validates, False otherwise
        :rtype: bool
        """

        for key, value in data.iteritems():
            if key in self.schema:
                types = self.schema.get(key)

                if isinstance(types, list):
                    for t in types:
                        if not isinstance(value, t):
                            return False
                else:
                    if not isinstance(value, types):
                        return False


class MembershipCheckingSchema(Schema):
    """
    Validates data against a schema, checking only for membership

    This will fail in the following situations:
    * If a key is in the data but not in the schema
    * If a key is in the schema but not in the data, and the schema doesn't
      allow None as a type for that data value
    """

    def validate(self, data):
        """
        Validates a data dictionary against the stored schema dictionary

        :param data: The data to check
        :type data: dict

        :return: True if the data validates, False otherwise
        :rtype: bool
        """

        for key in data.iterkeys():
            if key not in self.schema:
                return False

        for key, value in self.schema.iteritems():
            if key not in data:
                if isinstance(value, list):
                    if None not in value:
                        return False
                else:
                    if value is not None:
                        return False
