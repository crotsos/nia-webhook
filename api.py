import dialogflow_v2 as dialogflow

PROJECT_ID = "nira-68681"

ENTITY_TYPES_CACHE = []

"""
    INTENTS
"""


def list_intents():
    client = dialogflow.IntentsClient()
    parent = client.project_agent_path(PROJECT_ID)

    return list(client.list_intents(parent))


"""
    ENTITY TYPES
"""


def get_entity_type_id(display_name):
    """Get entity type id"""
    entity_types = list_entity_types()
    entity_type_id = None
    for entity_type in entity_types:
        if entity_type.display_name == display_name:
            entity_type_id = entity_type.name.split('/entityTypes/')[1]
    return entity_type_id


def list_entity_types():
    """List all entity types"""
    global ENTITY_TYPES_CACHE
    if not ENTITY_TYPES_CACHE:
        client = dialogflow.EntityTypesClient()
        parent = client.project_agent_path(PROJECT_ID)
        ENTITY_TYPES_CACHE = list(client.list_entity_types(parent))
    return ENTITY_TYPES_CACHE


def get_entity_type(entity_type_id):
    """Get entity type by id"""
    client = dialogflow.EntityTypesClient()
    name = client.entity_type_path(PROJECT_ID, entity_type_id)

    return client.get_entity_type(name)


def create_entity_type(display_name, kind):
    """Create an entity type with the given display name."""
    client = dialogflow.EntityTypesClient()

    parent = client.project_agent_path(PROJECT_ID)
    entity_type = dialogflow.types.EntityType(display_name=display_name, kind=kind)

    response = client.create_entity_type(parent, entity_type)

    print('Entity type created: \n{}'.format(response))


"""
    ENTITIES
"""


def create_entity(entity_type_id, entity_value, synonyms):
    """Create an entity of the given entity type."""
    client = dialogflow.EntityTypesClient()
    # Note: synonyms must be exactly [entity_value] if the
    # entity_type's kind is KIND_LIST
    synonyms = synonyms or [entity_value]
    entity_type_path = client.entity_type_path(PROJECT_ID, entity_type_id)

    entity = dialogflow.types.EntityType.Entity()
    entity.value = entity_value
    entity.synonyms.extend(synonyms)

    response = client.batch_create_entities(entity_type_path, [entity])
    print('Entity created: \n{}'.format(response))
