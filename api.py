""" Class for Dialogflow API client """

import dialogflow_v2 as dialogflow


class Dialogflow(object):
    """ Client for Dialogflow API methods """

    def __init__(self):
        self.project_id = "nira-68681"
        self.entity_types_cache = []

    """
        INTENTS
    """

    def list_intents(self):
        """ List all intents from chatbot """
        client = dialogflow.IntentsClient()
        parent = client.project_agent_path(self.project_id)

        return list(client.list_intents(parent))

    """
        ENTITY TYPES
    """

    def get_entity_type_id(self, display_name):
        """ Get entity type id """
        entity_types = self.list_entity_types()
        entity_type_id = None
        for entity_type in entity_types:
            if entity_type.display_name == display_name:
                entity_type_id = entity_type.name.split("/entityTypes/")[1]
        return entity_type_id

    def list_entity_types(self):
        """ List all entity types """
        if not self.entity_types_cache:
            client = dialogflow.EntityTypesClient()
            parent = client.project_agent_path(self.project_id)
            self.entity_types_cache = list(client.list_entity_types(parent))
        return self.entity_types_cache

    def get_entity_type(self, entity_type_id):
        """ Get entity type by id """
        client = dialogflow.EntityTypesClient()
        name = client.entity_type_path(self.project_id, entity_type_id)

        return client.get_entity_type(name)

    def create_entity_type(self, display_name, kind):
        """Create an entity type with the given display name."""
        client = dialogflow.EntityTypesClient()

        parent = client.project_agent_path(self.project_id)
        entity_type = dialogflow.types.EntityType(display_name=display_name, kind=kind)

        response = client.create_entity_type(parent, entity_type)

        print "Entity type created:\n{}".format(response)

    """
        ENTITIES
    """

    def create_entity(self, entity_type_id, entity_value, synonyms):
        """Create an entity of the given entity type."""
        client = dialogflow.EntityTypesClient()
        # Note: synonyms must be exactly [entity_value] if the
        # entity_type"s kind is KIND_LIST
        synonyms = synonyms or [entity_value]
        entity_type_path = client.entity_type_path(self.project_id, entity_type_id)

        entity = dialogflow.types.EntityType.Entity()
        entity.value = entity_value
        entity.synonyms.extend(synonyms)

        response = client.batch_create_entities(entity_type_path, [entity])
        print "Entity created: \n{}".format(response)
