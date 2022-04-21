from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from crm.models import Lead, Agent
from users.models import CustomUser


@registry.register_document
class LeadDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'lead'
        # See Elasticsearch Indices API reference for available settings
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    assignee = fields.ObjectField(properties={
        'user': fields.ObjectField(
            properties={
                'id': fields.IntegerField(),
                'first_name': fields.TextField(),
                'last_name': fields.TextField(),
                'email': fields.TextField(),
                'date_created': fields.DateField(),
                'date_updated': fields.DateField()

            })
    }
    )

    class Django:
        model = Lead  # The model associated with this Document
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'stage',
            'source',
            'gender',
            'marital_status',
            'date_created',
            'date_updated',
            'is_customer',
        ]
        related_models = [Agent]

    def get_queryset(self):
        return super(LeadDocument, self).get_queryset().select_related(
            'assignee'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Lead):
            return related_instance.agent_set.all()

    def prepare_sources(self, instance):
        print('Inside Lead Documents')
        print(instance.__dict__)
        exit()


@registry.register_document
class AgentDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'agent'
        # See Elasticsearch Indices API reference for available settings
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
        'email': fields.TextField(),
        'date_created': fields.DateField(),
        'date_updated': fields.DateField()
    })

    class Django:
        model = Agent  # The model associated with this Document
        fields = [
            'id'
        ]
        related_models = [CustomUser]

    def get_queryset(self):
        return super(AgentDocument, self).get_queryset().select_related(
            'user'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Agent):
            return related_instance.agent_set.all()

    def prepare_sources(self, instance):
        print('Inside Agent Documents')
        print(instance.__dict__)
        exit()
